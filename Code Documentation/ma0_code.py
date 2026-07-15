#original basic MA0 code ~ J.S (contact at https://github.com/JeetShannigrahi21/)

# SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
# SPDX-License-Identifier: BSD-3-Clause

"""
Code implementing finite-temperature Momentum Average (MA0) approximation
for the 1D Holstein polaron  
================================================================
This has direct correspondence with the equations in the manuscript but is purposefully not 
optimised speed through parallelism (numba) etc.

 Request "optimised codes" from my 
GitHub for faster versions. Since each dw process is independent of each other, it is an embarassingly 
parallel case so using numba results in substantial speed-gain. For higher D, caching and memoization
also causes great increase in performance without losing accuracy.

--------------------------------------------------------------------------------
Manuscript
--------------------------------------------------------------------------------
    "The effective mass and lifetime of single Holstein polarons at finite
     temperatures", J. Shannigrahi, J. Bonca, M. Berciu.

Equation labels below refer to the main text (`M') and the
Supplemental Material (`S`).  All energies are in units of
the hopping t; we set hbar = k_B = 1.

Holstein Model:
    H = -t sum_<ij> c_i^dag c_j  +  Omega sum_i b_i^dag b_i
        +  g sum_i c_i^dag c_i (b_i^dag + b_i)
    dimensionless coupling   lambda = g^2 / (2 D t Omega),   D = 1 here,
    so                       g = sqrt(lambda * 2 t Omega).

--------------------------------------------------------------------------------
Requirements (as of June 2026)
--------------------------------------------------------------------------------
    Python >= 3.9       (typically run with v3.12.11 on a 16 core Windows PC)
    numpy  >= 1.20     (tested with v2.4.1)
    matplotlib         (just for plotting)
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

# =============================================================================
# 1.  Local (momentum-averaged) free propagator  g0(omega)
# =============================================================================
def g0_local_1D(omega, t=1.0):
    r"""1D momentum-averaged free propagator  \bar g_0^{1D}(omega).

    Supplemental Material, "g0 expressions":
        \bar g_0^{1D}(omega) = sgn(omega) / sqrt((omega + i eta)^2 - 4 t^2).

        g0(z) = 1 / ( sqrt(z - 2t) * sqrt(z + 2t) ),      z = omega + i eta,

    `omega` is passed already complex (omega + i eta).
    """
    return 1.0 / (np.sqrt(omega - 2.0 * t) * np.sqrt(omega + 2.0 * t))


# =============================================================================
# 2.  Boltzmann weights for the on-site phonon number n_l
# =============================================================================
def boltzmann_weights(T, Omega, n_max=31):
    r"""Weights  w(n_l) = e^{-beta Omega n_l} / Z  of the thermal average
    <...>_th over the number n_l of pre-existing phonons on the active site
    (main text Eq. for <...>_th; partition function Z = sum_n e^{-beta Omega n}).

    Truncated at n_max Fock states (n_max = 31 was foun d to sufficient up to T ~ Omega).
    """

    if T == 0:
        w = np.zeros(n_max)
        w[0] = 1.0
        return w

    beta = 1.0 / T        
         
    q = np.exp(-beta * Omega)                   #note T is defined in units of t here instead of Omega
    n = np.arange(n_max)
    Z = np.sum(q ** n)                            # partition function
    
    return (q ** n) / Z
    


# =============================================================================
# 3.  MA(0) continued fractions  a_1(n_l, omega),  b_1(n_l, omega)
#     and the on-site amplitude  A(n_l, omega)
# =============================================================================
def a1_MA0(n_l, omega, g, Omega, t, M):
    r"""Emission-branch continued fraction  a_1(n_l, omega).

    Supplemental Material Eq.(S1 and S3):
        a_m = (m + n_l) g g0(omega - m Omega)
              / [ 1 - g g0(omega - m Omega) a_{m+1} ],
    evaluated from the top floor m = M (a_{M+1} = 0) down to m = 1.
    Returns a_1.
    """
    a_next = 0.0 + 0.0j                           # a_{M+1} = 0
    for m in range(M, 0, -1):
        g0m = g0_local_1D(omega - m * Omega, t)
        denom = (1.0 - g * g0m * a_next)
        if denom == 0:
            denom = 1e-30 + 0j
        a_next = (m + n_l) * g * g0m /denom
    return a_next                                 # = a_1


def b1_MA0(n_l, omega, g, Omega, t):
    r"""Annihilation-branch continued fraction  b_1(n_l, omega).

    Supplemental Material Eq.(S2) / Eq.(S4):
        b_m = (n_l - m + 1) g g0(omega + m Omega)
              / [ 1 - g g0(omega + m Omega) b_{m+1} ].
    The branch terminates naturally at m = n_l (the numerator vanishes for
    m = n_l + 1), so b_1(n_l = 0) = 0 exactly -- recovering the T = 0 limit.
    """
    if n_l == 0:
        return 0.0 + 0.0j                       
    b_next = 0.0 + 0.0j                           
    for m in range(n_l, 0, -1):
        g0m = g0_local_1D(omega + m * Omega, t)
        denom = (1.0 - g * g0m * b_next)
        if denom == 0:
            denom = 1e-30 + 0j
        b_next = (n_l - m + 1) * g * g0m / denom
    return b_next                                


def A_MA0(n_l, omega, g, Omega, t, M):
    r"""On-site amplitude  A(n_l, omega) = g [ a_1(n_l, omega) + b_1(n_l, omega) ].
    Main text Eq.(M4).
    """
    return g * (a1_MA0(n_l, omega, g, Omega, t, M)
                + b1_MA0(n_l, omega, g, Omega, t))


def sigma_MA0(omega, g, Omega, t, weights, M, thermal_cutoff=1e-8):
    r"""MA(0) self-energy  Sigma^{(0)}_T(omega).

    epsilon(omega)  (End Matter Eq.(M7)):
        epsilon = < A(n_l, omega) / (1 - g0(omega) A(n_l, omega)) >_th

    Sigma^{(0)}_T (main text Eq.(M2)):
        Sigma^{(0)}_T = epsilon / (1 + g0(omega) epsilon)
    """
    g0 = g0_local_1D(omega, t)
    eps = 0.0 + 0.0j
    for n_l, w in enumerate(weights):
        if w < thermal_cutoff:                    
            break
        A = A_MA0(n_l, omega, g, Omega, t, M)
        eps += w * (A / (1.0 - g0 * A))           # thermal average, Eq.(M7)
    return eps / (1.0 + g0 * eps)                 # Eq.(M2)



# =============================================================================
# 4.  Spectral function  A(k, omega) = -Im G(k, omega) / pi
# =============================================================================
def MA0_spectral_function(k, T, lam, Omega,directory,
                      t=1.0, eta=0.001,
                      omega_min=-5.0, omega_max=2.0,
                      M=75, n_max=31, thermal_cutoff=1e-8):
    r"""Compute Sigma_T(omega), G(k,omega) and A(k,omega) on a fequency grid.

    Green's function :
        G(k, omega) = 1 / (omega + i eta - eps_k - Sigma_T(omega)),
        eps_k       = -2 t cos(k a),      a = 1,
        A(k, omega) = -(1/pi) Im G(k, omega).

    Parameters
    ----------
    Returns (omega_real, A, Sigma) as NumPy arrays.
    """
    g = np.sqrt(lam * 2.0 * t * Omega)            # lambda = g^2/(2 t Omega), D=1
    weights = boltzmann_weights(T, Omega, n_max)

    dw = eta / 5.0
    omega_array = np.arange(omega_min, omega_max, dw)
    omega_cplx = omega_array + 1j * eta

    
    Sigma = np.array([sigma_MA0(w, g, Omega, t, weights, M, thermal_cutoff)
                      for w in omega_cplx])

    eps_k = -2.0 * t * np.cos(k)
    G = 1.0 / (omega_cplx - eps_k - Sigma)
    A = -np.imag(G) / np.pi

    # --- pickle data saving and writing---

    data = {
            "params": {
                "t": t,
                "Omega": Omega,
                "lam": lam,
                "T": T,
                "eta": eta,
                "M":M,
                "k": k,
                "eps_k": eps_k
            },
            "weights": weights,
            "omega_vals": omega_array,
            "Self_energy": Sigma,
            "G_T": G,
            "A_spectral": A
        }

    file_name =  f"MA0_1D_T{T:.3f}_k({k:.3f})_Omega{Omega:.3f}_lam{lam:.3f}.pkl"
    file_path = os.path.join(directory, file_name)
    with open(file_path, "wb") as f:
        pickle.dump(data, f)


    # --- plotting ---
    
    fig_name =  f"MA0_1D_T{T:.3f}_k({k:.3f})_Omega{Omega:.3f}_lam{lam:.3f}.png"
    fig_path = os.path.join(directory, fig_name)
    
    plt.figure()
    plt.plot(omega_array, A, color = 'g', label=r"$A(k,\omega)$")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$A(k,\omega)$")
    plt.title(fr"MA0 1D, T = {T:.3f}")
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(fig_path, dpi=500, bbox_inches="tight")
    plt.close() 

    return omega_array, A, Sigma


# =============================================================================
# 5.  Demo run
# =============================================================================

lam = 1.25
Omega = 1.0
k = 0

M = 75            # max. no of phonons in a1_MA0. Estimate is g**2/Omega**2 
                    # but taken quite higher for safe convergence

T = 0.5 #defined in terms of t
eta = 0.005

directory = "MA0_data_1D" #saving location, use import os or pathlib.Path
os.makedirs(directory, exist_ok=True)
w, A, Sig = MA0_spectral_function(k, T, lam, Omega, directory, M=M, eta=eta, omega_min=-5, omega_max=2)

