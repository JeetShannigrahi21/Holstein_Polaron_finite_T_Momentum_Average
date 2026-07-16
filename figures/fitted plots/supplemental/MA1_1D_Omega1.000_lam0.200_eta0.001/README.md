# MA1_1D_Omega1.000_lam0.200_eta0.001

MA(1) 1D Holstein-polaron spectral fits at k=0, Omega=1.0t, lambda=0.2, eta0=0.001. This is one of the m*/eta* vs T curves of Fig. 3 / S12 / S13, and provides the per-temperature spectra and their multi-Lorentzian fits.

Data are truncated at the regime-of-certainty **T_cutoff = 0.225 t** (T/Omega = 0.225) used in the paper.

## `pickle data/`
Per-temperature MA(1) spectral pickles `A(omega, k=0)` (one per T up to the cutoff). Load as described in the top-level `README.md` (`d['omega_vals']`, `d['A_spectral']`, `d['Self_energy']`, `d['params']`).

## `fitted data/`
- `gs_data_vs_T_lam0.2_Omega1.0_MA1.txt` -- combined table vs temperature: `T`, `k`, `QP_weight` ( Z, so m*/m0 = 1/Z ), `eta*`, `gs_energy`, fit `R2`, and per-parameter fit errors. Truncated at the cutoff.
- `fig_fit_T*.png` -- the individual multi-Lorentzian fit of the k=0 spectrum at each temperature (the actual fit plots; trend plots are not included).


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../../LICENSES/CC-BY-4.0.txt`.
