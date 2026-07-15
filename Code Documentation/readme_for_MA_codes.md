
## Conventions

| Symbol | Meaning | Code | Additional notes |
|---|---|---|---|
| `t` | hopping (energy unit) | `t=1.0` |
| `Ω` | Einstein phonon frequency | `Omega` |
| `λ` | dimensionless coupling | `lam` | `λ = g²/(2Dt·Ω)` |
| `g` | bare e–ph coupling | `g = np.sqrt(lam*2*D*t*Omega)` | in 1D `D=1` so `g=√(2λtΩ)` this is Dimension dependent
| `η₀` | artificial broadening | `eta`, used as `ω+iη` |  `Ĝ(ω)=[ω+iη₀−Ĥ]⁻¹` |
| `ε_k` | free dispersion | `-2t*cos(k*a)` | `ε_k = −2t cos k` (1D) but Dimension dependent
| `g₀(ω)` | on-site free propagator | `G0_loc(ω,t)` | Dimension dependent


### Notes:
- The truncation `n_max = 31` and cutoff `thermal_cutoff = 1e-8` are convergence
parameters.

Limits verified analytically in the manuscript and reproduced by the code:
- **`t → 0` (atomic limit):** exact for any `T`, any `λ`.
- **`T → 0`:** only `weights[0]=1` survives, `b₁→0`, and `Σ⁽⁰⁾_T → A(0,ω)`, the
  T = 0 MA⁽⁰⁾ self-energy (see 2006 paper).
- MA⁽¹⁾ changes: MA⁽¹⁾  renormalises the continued
fractions `a₁→ã₁`, `b₁→b̃₁`. The extra phonon "outside the cloud" is threaded in through the auxiliary propagators `F₁`, `G_B`, `G_E`.

##  Convergence parameters:
| Parameter | Value | safe convergence |
|---|---|---|
| `M` | 75 | continued-fraction / cloud depth. Rule of thumb `M >> g²/Ω² = 8Dλ/Ω`, `M=75` is converged across for all reasonabe coupling/adiabatic cases.
| `n_max` | 31 | phonon Fock states in ⟨·⟩_th;  |
| `thermal_cutoff` | 1e-8 |
| `dw` | `η/5` | frequency spacing of the `ω`-grid. Finer grid allows for better fitting|


