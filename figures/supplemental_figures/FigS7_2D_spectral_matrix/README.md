# FigS7_2D_spectral_matrix

## Plotted parameters
Method: MA(1) (2D). 2D, t=1, eta0=0.01; Omega in {0.5,1.0,2.0}; lambda in {0.5,1.0,1.5}; T/Omega in {0,0.2,0.3,0.5,0.75,1.0}.
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
- **Panel (Om0.5_lam0.50)**: Omega=0.5 t, lambda=0.5, eta0=0.01
  - Temperatures (T/Omega): 0.000, 0.200, 0.300, 0.500, 0.750, 1.000
  - omega grid: wmin=-10.0000 t, wmax=-0.0033 t, dw=0.00333 t, N=3000
- **Panel (Om0.5_lam1.00)**: Omega=0.5 t, lambda=1, eta0=0.01
  - Temperatures (T/Omega): 0.000, 0.200, 0.300, 0.500, 0.750, 1.000
  - omega grid: wmin=-10.0000 t, wmax=-0.0033 t, dw=0.00333 t, N=3000
- **Panel (Om0.5_lam1.50)**: Omega=0.5 t, lambda=1.5, eta0=0.01
  - Temperatures (T/Omega): 0.000, 0.200, 0.300, 0.500, 0.750, 1.000
  - omega grid: wmin=-10.0000 t, wmax=-0.0033 t, dw=0.00333 t, N=3000
- **Panel (Om1.0_lam0.50)**: Omega=1 t, lambda=0.5, eta0=0.01
  - Temperatures (T/Omega): 0.000, 0.200, 0.300, 0.500, 0.750, 1.000
  - omega grid: wmin=-10.0000 t, wmax=-0.0033 t, dw=0.00333 t, N=3000
- **Panel (Om1.0_lam1.00)**: Omega=1 t, lambda=1, eta0=0.01
  - Temperatures (T/Omega): 0.000, 0.200, 0.300, 0.500, 0.750, 1.000
  - omega grid: wmin=-10.0000 t, wmax=-0.0033 t, dw=0.00333 t, N=3000
- **Panel (Om1.0_lam1.50)**: Omega=1 t, lambda=1.5, eta0=0.01
  - Temperatures (T/Omega): 0.000, 0.200, 0.300, 0.500, 0.750, 1.000
  - omega grid: wmin=-10.0000 t, wmax=-0.0033 t, dw=0.00333 t, N=3000
- **Panel (Om2.0_lam0.50)**: Omega=2 t, lambda=0.5, eta0=0.01
  - Temperatures (T/Omega): 0.000, 0.200, 0.300, 0.500, 0.750, 1.000
  - omega grid: wmin=-10.0000 t, wmax=-0.0033 t, dw=0.00333 t, N=3000
- **Panel (Om2.0_lam1.00)**: Omega=2 t, lambda=1, eta0=0.01
  - Temperatures (T/Omega): 0.000, 0.200, 0.300, 0.500, 0.750, 1.000
  - omega grid: wmin=-10.0000 t, wmax=-0.0033 t, dw=0.00333 t, N=3000
- **Panel (Om2.0_lam1.50)**: Omega=2 t, lambda=1.5, eta0=0.01
  - Temperatures (T/Omega): 0.000, 0.200, 0.300, 0.500, 0.750, 1.000
  - omega grid: wmin=-10.0000 t, wmax=-0.0033 t, dw=0.00333 t, N=3000


---
*Part of the data repository for the manuscript; see the top-level `README.md` and
`DATA_AVAILABILITY.md`.*


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
