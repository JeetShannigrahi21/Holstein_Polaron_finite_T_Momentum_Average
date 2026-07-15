# FigS8_heatmap_1D_Om0.5

## Plotted parameters
Method: MA(1) (1D). 1D, Omega=0.5t, lambda=0.25, eta0=0.001; several T.
Grid spacing `dw ~ eta0/5`.

## Files in each panel folder
- `*.pkl` -- one pickle per temperature holding the FULL 2-D spectral map `A_kw` of shape `(Nw, Nk)` plus the `omega_vals` and `k_vals` axes (the matrix is too large for CSV). `A_kw` is stored as float32.
- `omega_grid.csv`, `k_grid.csv` -- the `omega/t` and `k/pi` (+`k`) axes.
- `A_omega_kslices_T*.csv` -- `omega/t` and `A(omega,k)` at a few representative momenta (k/pi = 0, 0.25, 0.5, 0.75, 1.0) for quick viewing.

## Pickle schema & how to open
Each `.pkl` is a Python `dict`. Load it with:

```python
import pickle, numpy as np
d = pickle.load(open('<one_T>.pkl','rb'))
omega = d['omega_vals']      # (Nw,) frequency grid, units of t
k     = d['k_vals']          # (Nk,) momenta in [0, pi]
Akw   = d['A_kw']            # (Nw, Nk) spectral function A(omega,k)
print(d['params'])           # {t, Omega, lam, T, eta, Nk, ...}
```

The `params` dict records `t, Omega, lambda, T, eta` and the momentum. Temperature
`T` is stored **in units of t**; figures label curves by `T/Omega` (both appear in
the CSV headers).

## Panels
- **Panel (Om0.5_lam0.25)**: Omega=0.5 t, lambda=0.25, eta0=0.001 -- A(omega,k) maps at T=0.000, 0.150, 0.250, 0.300, 0.500, 0.750. Full A_kw in the pickles; CSV gives axes + k-slices.


---
*Part of the data repository for the manuscript; see the top-level `README.md` and
`DATA_AVAILABILITY.md`.*


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
