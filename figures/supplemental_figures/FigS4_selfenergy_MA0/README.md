# FigS4_selfenergy_MA0

## Plotted parameters
Method: MA(0) (1D/2D/3D). same as FigS3_selfenergy_MA1.
Grid spacing `dw ~ eta0/5`.

## Files in each panel folder
- `spectral_A_k0*.csv` / `.txt` -- column 1 is `omega/t`; each further column is `A(omega, k=0)` at one temperature (header gives both `T` and `T/Omega`). These are the RAW curves; the vertical shift/scale in the figure is cosmetic and NOT applied here.
- `self_energy_k0*.csv` -- `omega/t` then `Re Sigma`, `Im Sigma` per T (when relevant).
- `*.pkl` -- one Python pickle per temperature (full object, see below).

## Pickle schema & how to open
Each `.pkl` is a Python `dict`. Load it with:

```python
import pickle, numpy as np
d = pickle.load(open('<one_of_the>.pkl','rb'))
omega = d['omega_vals']          # frequency grid, units of t
A     = d['A_spectral']          # A(omega, k) = -Im G / pi
Sig   = d['Self_energy']         # complex Sigma(omega)
print(d['params'])               # {t, Omega, lam, T, eta, k/kx, eps_k}
```

The `params` dict records `t, Omega, lambda, T, eta` and the momentum. Temperature
`T` is stored **in units of t**; figures label curves by `T/Omega` (both appear in
the CSV headers).

## Panels
- **Panel (1D)**: Omega=1.5 t, lambda=0.5, eta0=0.001
  - Temperatures (T/Omega): 0.001, 0.333, 0.667, 1.000
  - omega grid: wmin=-7.0000 t, wmax=4.9997 t, dw=0.00033 t, N=36000
- **Panel (2D)**: Omega=2 t, lambda=0.5, eta0=0.001
  - Temperatures (T/Omega): 0.001, 0.150, 0.375, 0.750
  - omega grid: wmin=-11.0000 t, wmax=3.9997 t, dw=0.00033 t, N=45000
- **Panel (3D)**: Omega=2.5 t, lambda=0.5, eta0=0.005
  - Temperatures (T/Omega): 0.000, 0.200, 0.400, 0.600
  - omega grid: wmin=-13.0000 t, wmax=-0.0025 t, dw=0.00250 t, N=5200


---
*Part of the data repository for the manuscript; see the top-level `README.md` and
`DATA_AVAILABILITY.md`.*


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
