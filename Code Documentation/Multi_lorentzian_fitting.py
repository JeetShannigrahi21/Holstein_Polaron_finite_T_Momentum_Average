#original code ~ J.S (contact at https://github.com/JeetShannigrahi21/)

# SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
# SPDX-License-Identifier: BSD-3-Clause

from lmfit.models import LorentzianModel
# from https://lmfit.github.io/lmfit-py/
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pickle
import math
import re


T_cutoff = 0.450 #set whichever value  you wish
offset = 600 #no of dw points around the QP peak
# ------------------------------------------------------------
def find_k0_leftmost_peak(w, A_k0):
    """
    Given a spectrum A(ω), choose the leftmost peak
    (smallest-ω local maximum) and return its ω position.

    Returns
    -------
    E0_k0 : float
        Baseline peak energy (ω of the leftmost peak).
        np.nan is returned if A_k0 has no finite entries.
    idx_peak : int
        Index of the chosen peak in the *sorted* ω array.
    """
    w = np.asarray(w, float)
    A = np.asarray(A_k0, float)

    if w.shape != A.shape:
        raise ValueError("w and A_k0 must have the same shape.")

    # Sort by ω just in case
    order = np.argsort(w)
    if not np.array_equal(order, np.arange(w.size)):
        w = w[order]
        A = A[order]

    if not np.isfinite(A).any():
        return math.nan, -1

    def _local_maxima_indices(y: np.ndarray):
        """Strict local maxima indices."""
        if y.size < 3:
            return []
        return [
            i for i in range(1, y.size - 1)
            if y[i] > y[i - 1] and y[i] > y[i + 1]
        ]

    # Replace NaNs with 0 for peak search
    y_clean = np.where(np.isfinite(A), A, 0.0)

    # 1) all local maxima
    idx_local = _local_maxima_indices(y_clean)

    if idx_local:
        # choose the smallest ω among them → leftmost peak
        i_pick = min(idx_local, key=lambda i: w[i])
        return float(w[i_pick]), int(i_pick)

    # 2) no internal local maxima → fall back to global maximum
    j = int(np.nanargmax(y_clean))
    return float(w[j]), j


# ------------------------------------------------------------
def build_window(omega, center, halfwidth=0.25):
    """
    Choose indices [left_i, right_i] such that
    omega[left_i] ≈ center - halfwidth
    omega[right_i] ≈ center + halfwidth.
    """
    omega = np.asarray(omega, float)
    left_val = center - halfwidth
    right_val = center + halfwidth

    left_i = int(np.searchsorted(omega, left_val, side="left"))
    right_i = int(np.searchsorted(omega, right_val, side="right") - 1)

    left_i = max(0, left_i)
    right_i = min(omega.size - 1, right_i)

    if right_i <= left_i:
        # fallback: use the whole array
        left_i, right_i = 0, omega.size - 1

    return left_i, right_i

def run_four_lorentz_fits(parent_dir):
    parent_dir = Path(parent_dir)

    pkl_files = sorted(parent_dir.glob("MA1_1D_T*_k0.000_*.pkl"))
    if not pkl_files:
# %
        raise FileNotFoundError(f"No MA1_1D_T*_k0_*.pkl found in {parent_dir}")


    entries = []
    for fn in pkl_files:
        with open(fn, "rb") as f:
            d = pickle.load(f)
        T = float(d["params"]["T"])
        entries.append((T, fn, d))
    entries.sort(key=lambda x: x[0])

    first_params = entries[0][2]["params"]
    lam = float(first_params["lam"])
    Omega = float(first_params["Omega"])
    eta_global = float(first_params["eta"])

    root_fig_dir = parent_dir / "four_lorentz_figs_v1.3"
    output_dir = parent_dir / "four_lorentz_tables_v1.3"
    root_fig_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)

    fig_subdir_tpl = "T{T:.3f}"
    fig_file_tpl = (
        "fig_fit_T{T:.3f}_k{k:.3f}_Omega{Omega:.3f}_lam{lam:.3f}_eta{eta:.3f}.png"
    )

    # ========= baseline (T min) – 1 Lorentzian, NO background =========
    T0, fn0, d0 = entries[0]
    omega0 = np.asarray(d0["omega_vals"], float)
    A0 = np.asarray(d0["A_spectral"], float)
    eta0 = float(d0["params"]["eta"])
    k0 = float(d0["params"]["k"])

    E0_guess, idx0 = find_k0_leftmost_peak(omega0, A0)
    if idx0 < 0:
        raise RuntimeError("Baseline spectrum has no finite entries / peaks.")

    idx0 = int(idx0)
    prev_peak_position = float(omega0[idx0])

    prev_w = eta0 #float(max(gamma_from_SE, 1e-6))

    left_i0, right_i0 = build_window(omega0, prev_peak_position, halfwidth=0.25)
    left_i0 = left_i0 - offset
    right_i0 = right_i0 + offset
    omega_fit0 = omega0[left_i0:right_i0 + 1]
    A_fit0 = A0[left_i0:right_i0 + 1]

    lor1_simple = LorentzianModel(prefix="p1_")
    model_simple = lor1_simple  # no ConstantModel

    params0 = model_simple.make_params()
    guess0 = lor1_simple.guess(A_fit0, x=omega_fit0)
    for name, par in guess0.items():
        if name in params0:
            params0[name].set(value=par.value)

    params0["p1_center"].set(value=prev_peak_position)
    params0["p1_sigma"].set(value=prev_w)

    result0 = model_simple.fit(
        A_fit0,
        params0,
        x=omega_fit0,
        method="least_squares",
        nan_policy="omit",
    )

    prev_A = result0.params["p1_amplitude"].value
    prev_peak_position = result0.params["p1_center"].value
    prev_w = result0.params["p1_sigma"].value

    print(
        f"Baseline (simple) fit at T={T0:.3f}: "
        f"A={prev_A:.6g}, E={prev_peak_position:.6g}, w={prev_w:.6g}"
    )
    table_file_tpl = "gs data for T{T:.3f} for lambda {lam} and Omega {Omega}.txt"
    fmt = (
        "%10.3f "
        "%12.6e "
        "%12.6e "
        "%12.6e "
        "%10.6f "
        "%12.6e "
        "%12.6e "
        "%12.6e"
    )

    # errors on amplitude/center from the baseline fit
    sigma_A1_0 = result0.params["p1_amplitude"].stderr or np.nan
    sigma_E1_0 = result0.params["p1_center"].stderr or np.nan
    sigma_w1_0 = np.nan   # width not a fitted parameter at baseline

    # R^2 for the baseline fit
    L1_0 = result0.eval(x=omega_fit0)   # best-fit 1-Lorentzian on the baseline window
    ss_res_0 = np.sum((A_fit0 - L1_0) ** 2)
    ss_tot_0 = np.sum((A_fit0 - np.mean(A_fit0)) ** 2)
    R2_0 = 1.0 - ss_res_0 / ss_tot_0 if ss_tot_0 > 0 else np.nan

    # metrics row: (k, QP_weight, eta*, gs_energy, R2, err_A1, err_w1, err_E1)
    metrics_arr0 = np.array(
        [[k0, prev_A, prev_w, prev_peak_position,
          R2_0, sigma_A1_0, sigma_w1_0, sigma_E1_0]],
        dtype=float,
    )

    table_file0 = output_dir / table_file_tpl.format(T=T0, lam=lam, Omega=Omega)
    np.savetxt(
        table_file0,
        metrics_arr0,
        fmt=fmt,
        header=(
            "k          QP_weight      eta*          gs_energy     R2       "
            "error_A1      error_w1       error_E1"
        ),
        comments="",
    )

    fig_subdir = root_fig_dir
    fig_subdir.mkdir(parents=True, exist_ok=True)

    omega_hr0 = omega_fit0  # high-res x for the fitted Lorentzian
    plt.figure(figsize=(12, 12))
    plt.plot(omega0, A0, lw=1.0, label="Spectrum")
    plt.plot(omega_hr0, L1_0, lw=0.8, label="Sum_fit = Lorentzian 1")
    plt.axvline(prev_peak_position, ls="--", lw=1.0, label="GS peak")
    plt.axvline(omega0[left_i0], ls=":", lw=0.7, label="left edge")
    plt.axvline(omega0[right_i0], ls=":", lw=0.7, label="right edge")
    plt.legend(loc="upper left", fontsize=8)
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$A(\omega)$")
    plt.title(f"Baseline 1-Lorentzian Fit at k={k0:.3f}, T={T0:.3f}")
    plt.tight_layout()

    fig_file0 = fig_subdir / fig_file_tpl.format(
        T=T0, lam=lam, Omega=Omega, eta=eta0, k=k0
    )
    plt.savefig(fig_file0, dpi=150)
    plt.close("all")
    print(f"  • Saved baseline fit → {fig_file0}")
    print(f"→ Saved baseline table → {table_file0}")
    # ================== full 3-Lorentzian fit, no background ==================
    for T, fn, d in entries[1:]:
        print(f"\n=== T = {T:.3f}, file = {fn.name} ===")
        if (T>T_cutoff):
            break
        omega = np.asarray(d["omega_vals"], float)
        A = np.asarray(d["A_spectral"], float)

        k = float(d["params"]["k"])
        eta = float(d["params"]["eta"])

        left_i, right_i = build_window(omega, prev_peak_position, halfwidth=0.25)
        left_i = left_i - offset
        right_i = right_i + offset
        omega_fit = omega[left_i:right_i + 1]
        A_fit = A[left_i:right_i + 1]
        width_i = right_i - left_i
        width_in_w =(width_i*(omega[1]-omega[0]))/2
        if omega_fit.size < 5:
            print(f"[WARN] Too few points in window at T={T:.3f}, skipping.")
            continue

        # 3 Lorentzians only
        lor1 = LorentzianModel(prefix="p1_")
        lor2 = LorentzianModel(prefix="p2_")
        lor3 = LorentzianModel(prefix="p3_")
        lor4 = LorentzianModel(prefix="p4_")
        model = lor1 + lor2 + lor3 + lor4

        params = model.make_params()

        # main peak: guesses from previous T
        A1_guess = prev_A
        E1_guess = prev_peak_position
        w1_guess = prev_w #float(max(gamma_from_SE, 1e-6))
        
        
       
        params["p1_amplitude"].set(
            value=A1_guess,
            min=0.3 * prev_A,
            max=1.5 * prev_A,
        )

        params["p1_center"].set(
            value=E1_guess,
            min=prev_peak_position - 0.05,
            max=prev_peak_position + 0.1,
        )
        params["p1_sigma"].set(
            value=w1_guess,
            min=0.75*prev_w,
            max=3.0 * prev_w,
        )

        # thermal peaks
        A2_guess = 0.1 * A1_guess
        A3_guess = 0.2 * A1_guess
        A4_guess = 0.2 * A1_guess
        
        params["p2_amplitude"].set(
            value=A2_guess,
            min=0.0,
            max=0.5 * prev_A,
        )
        params["p3_amplitude"].set(
            value=A3_guess,
            min=0.0,
            max=0.5 * prev_A,
        )
        params["p4_amplitude"].set(
            value=A4_guess,
            min=0.0,
            max=0.5 * prev_A,
        )
        
        # --- centers tied to main peak center ---
        params.add("deltaE2", value=0.025, min=0.005,  max=width_in_w)
        params.add("deltaE3", value=-0.05, min=-width_in_w, max=-0.025)
        params.add("deltaE4", value=0.1, min=0.05, max=width_in_w)
        
        params["p2_center"].set(expr="p1_center + deltaE2")
        params["p3_center"].set(expr="p1_center + deltaE3")
        params["p4_center"].set(expr="p1_center + deltaE4")
        
        # --- widths tied to main peak width ---
        params.add("w2_factor", value=10.0, min=1.25, max=500.0)
        params.add("w3_factor", value=20.0, min=1.25, max=500.0)
        params.add("w4_factor", value=5.0, min=1.25, max=500.0)
        
        params["p2_sigma"].set(expr="w2_factor * p1_sigma")
        params["p3_sigma"].set(expr="w3_factor * p1_sigma")
        params["p4_sigma"].set(expr="w4_factor * p1_sigma")
        # fit
        result = model.fit(
            A_fit,
            params,
            x=omega_fit,
            method="least_squares",
            nan_policy="omit",
            max_nfev=50000,
        )

        if not result.success:
            print(f"[WARN] Fit at T={T:.3f} failed: {result.message}")
            continue

        p = result.params
        A1 = p["p1_amplitude"].value
        w1 = p["p1_sigma"].value
        E1 = p["p1_center"].value

        A2 = p["p2_amplitude"].value
        w2 = p["p2_sigma"].value
        E2 = p["p2_center"].value

        A3 = p["p3_amplitude"].value
        w3 = p["p3_sigma"].value
        E3 = p["p3_center"].value
        
        A4 = p["p4_amplitude"].value
        w4 = p["p4_sigma"].value
        E4 = p["p4_center"].value

        sigma_A1 = p["p1_amplitude"].stderr or np.nan
        sigma_w1 = p["p1_sigma"].stderr or np.nan
        sigma_E1 = p["p1_center"].stderr or np.nan

        omega_hr = omega_fit
        comps = result.eval_components(x=omega_hr)
        L1 = comps["p1_"]
        L2 = comps["p2_"]
        L3 = comps["p3_"]
        L4 = comps["p4_"]
        Lsum = L1 + L2 + L3  + L4# no y0

        ss_res = np.sum((A_fit - Lsum) ** 2)
        ss_tot = np.sum((A_fit - np.mean(A_fit)) ** 2)
        R2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else np.nan

        print(
            f"Fit at T={T:.3f}: "
            f"A1={A1:.6g}, w1={w1:.6g}, E1={E1:.6g}, R2={R2:.6f}"
        )

        # metrics row (k is always 0 here)
        metrics_arr = np.array(
            [[k, A1, w1, E1, R2, sigma_A1, sigma_w1, sigma_E1]],
            dtype=float,
        )

        table_file_tpl = "gs data for T{T:.3f} for lambda {lam} and Omega {Omega}.txt"
        table_file = output_dir / table_file_tpl.format(T=T, lam=lam, Omega=Omega)
        fmt = (
            "%10.3f "
            "%12.6e "
            "%12.6e "
            "%12.6e "
            "%10.6f "
            "%12.6e "
            "%12.6e "
            "%12.6e"
        )
        np.savetxt(
            table_file,
            metrics_arr,
            fmt=fmt,
            header=(
                "k          QP_weight      eta*          gs_energy     R2       "
                "error_A1      error_w1       error_E1"
            ),
            comments="",
        )
       

        # plotting (no background)
        fig_subdir = root_fig_dir
        fig_subdir.mkdir(parents=True, exist_ok=True)

        plt.figure(figsize=(16, 16))
        plt.plot(omega_hr, A_fit, lw=1.2, label="Spectrum")
        plt.plot(omega_hr, L1, lw=1.5, label="Lorentzian 1")
        plt.plot(omega_hr, Lsum, lw=1.0, label="Sum fit")
        plt.axvline(E1, ls="--", lw=1.3, label="GS peak")
        plt.axvline(E2, ls=":", lw=0.8, label="thermal_peak_1")
        plt.axvline(E3, ls=":", lw=0.8, label="thermal_peak_2")
        plt.axvline(E4, ls=":", lw=0.8, label="thermal_peak_3")
        plt.axvline(omega[left_i], ls=":", lw=1.2, label="left edge")
        plt.axvline(omega[right_i], ls=":", lw=1.2, label="right edge")
        plt.legend(loc="upper left", fontsize=8)
        plt.xlabel(r"$\omega$")
        plt.ylabel(r"$A(\omega)$")
        plt.title(f"Three-Lorentzian Fit at k={k:.3f}, T={T:.3f}")
        plt.tight_layout()

        fig_file = fig_subdir / fig_file_tpl.format(
            T=T, lam=lam, Omega=Omega, eta=eta, k=k
        )
        plt.savefig(fig_file, dpi=150)
        plt.close("all")
        print(f"  • Saved fit → {fig_file}")

        # seed next T
        prev_A = A1
        prev_w = w1
        prev_peak_position = E1
   
# --------- combine all per-T tables into one, with a T column ---------
    all_rows = []
    
    # pattern: "gs data for T0.400 for lambda 1.750 and Omega 0.750.txt"
    for fn in sorted(output_dir.glob("gs data for T* for lambda *.txt")):
        m = re.search(r"T([0-9.]+)\s+for\s+lambda", fn.name)
        if not m:
            print(f"[WARN] Could not parse T from filename: {fn.name}")
            continue
        T_val = float(m.group(1))
    
        arr = np.loadtxt(fn, skiprows=1)      
        arr = np.atleast_2d(arr)              
    
        T_col = np.full((arr.shape[0], 1), T_val)
        all_rows.append(np.hstack([T_col, arr]))
    
    if all_rows:
        combined = np.vstack(all_rows)
        # sort by T (column 0)
        combined = combined[np.argsort(combined[:, 0])]
    
        combined_file = output_dir / f"gs_data_vs_T_lam{lam:.3f}_Omega{Omega:.3f}_MA1.txt"
        np.savetxt(
            combined_file,
            combined,
            fmt="%.6e",
            header=(
                "T           k           QP_weight      eta*          gs_energy   "
                "R2          error_A1      error_w1      error_E1"
            ),
            comments="",
        )
      
        # --------- plot how QP_weight and eta* evolve with T ---------
        T_vals   = combined[:, 0]   # T
        QP_vals  = combined[:, 2]   # QP_weight
        eta_vals = combined[:, 3]   # eta*
    



