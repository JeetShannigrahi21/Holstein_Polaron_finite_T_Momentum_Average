# FigS10_m_star_fitting

## Plotted parameters
MA(1); temperature dependence of the effective mass m*/m0 fitted to a quadratic in the Bose factor n_B(Omega/T). Each panel is a different (dimension, Omega, lambda) case. The released CSV/TXT give the m*/m0 vs T data points that were fitted.

Fit model: `m*(T)/m0 = a n_B^2 + b n_B + c,   n_B = 1/(exp(Omega/T) - 1)`.
`n_B` is the Bose factor at the phonon frequency; `T`, `Omega` are in units of `t`.

## Files
- `panel_<x>_<dim>_Om<Omega>_lam<lambda>.csv` / `.txt` -- one file per panel, columns
  `T` (units of t), `T_over_Omega`, `n_B`, and the fitted quantity `mstar_over_m0`. These are
  the raw data points that were fitted (truncated at each case's T_cutoff).

## Fitted parameters (with 1-sigma standard errors)
- **(a)** 1D, Omega=1, lambda=1.75:  a = -95.597 +/- 5.7665,  b = 104.05 +/- 0.13286,  c = 5.7337  (R^2 = 1.00000, N = 10)
- **(b)** 3D, Omega=1, lambda=0.75:  a = 32.37 +/- 1.5476,  b = 2.0971 +/- 0.17154,  c = 1.2722  (R^2 = 0.99832, N = 18)
- **(c)** 2D, Omega=2, lambda=1.5:  a = -175.39 +/- 12.299,  b = 29.504 +/- 0.71961,  c = 2.1134  (R^2 = 0.99484, N = 29)
- **(d)** 3D, Omega=0.75, lambda=0.2:  a = 0.05037 +/- 0.00234,  b = 0.08219 +/- 0.00139,  c = 1.0448  (R^2 = 0.99933, N = 28)


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
