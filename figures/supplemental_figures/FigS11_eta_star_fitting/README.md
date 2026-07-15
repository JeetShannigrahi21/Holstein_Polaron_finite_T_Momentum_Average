# FigS11_eta_star_fitting

## Plotted parameters
MA(1); temperature dependence of the thermal broadening eta* = eta_T - eta_0 fitted to p n_B + q n_B^2. Each panel is a different (dimension, Omega, lambda) case. The released CSV/TXT give the eta* vs T data points that were fitted.

Fit model: `eta*(T) = p n_B + q n_B^2,   n_B = 1/(exp(Omega/T) - 1)`.
`n_B` is the Bose factor at the phonon frequency; `T`, `Omega` are in units of `t`.

## Files
- `panel_<x>_<dim>_Om<Omega>_lam<lambda>.csv` / `.txt` -- one file per panel, columns
  `T` (units of t), `T_over_Omega`, `n_B`, and the fitted quantity `eta_star`. These are
  the raw data points that were fitted (truncated at each case's T_cutoff).

## Fitted parameters (with 1-sigma standard errors)
- **(a)** 1D, Omega=0.75, lambda=0.75:  p = 0.07096 +/- 0.00497,  q = 0.16769 +/- 0.04586  (R^2 = 0.99650, N = 9)
- **(b)** 3D, Omega=0.75, lambda=0.5:  p = 0.24665 +/- 0.00369,  q = 0.33181 +/- 0.01615  (R^2 = 0.99970, N = 19)
- **(c)** 2D, Omega=2, lambda=1.125:  p = 0.15403 +/- 0.00278,  q = 0.12624 +/- 0.02526  (R^2 = 0.99914, N = 29)
- **(d)** 3D, Omega=1, lambda=0.2:  p = 0.12061 +/- 0.00021,  q = 0.08059 +/- 0.00103  (R^2 = 0.99999, N = 23)


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
