# FigS12_eff_mass_lifetime_Om1.0

## Plotted parameters
MA(1); m*/m0 and eta* = eta_T - eta_0 vs T for 1D, 2D, 3D at t=1, Omega=1.0t; eta0=0.001 (1D) and 0.01 (2D, 3D).
Temperature is shown in the paper as `T/Omega` (up to T ~ 0.75 Omega).

## Files in each panel folder (`panel_1D`, `panel_2D`, `panel_3D`)
- `mstar_eta_vs_T_<dim>.csv` / `.txt` -- columns: `lambda`, `T` (units of t),
  `T_over_Omega`, `mstar_over_m0` ( = m*/m0 = 1/Z ), `eta_star` ( = eta_T - eta_0,
  proportional to 1/tau ), and `T_cutoff` (the per-lambda regime-of-certainty upper
  temperature, in units of t, up to which each curve is shown).
- One block of rows per `lambda`; rows are already truncated at each lambda's
  `T_cutoff`. 
## Curves (per dimension)
- **1D**: lambda = 0.1, 0.2, 0.5, 0.75, 1.125, 1.25, 1.5, 1.75.
- **2D**: lambda = 0.1, 0.2, 0.5, 1.125, 1.25 .
- **3D**: lambda = 0.1, 0.2, 0.5, 0.75, 1.125 .


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
