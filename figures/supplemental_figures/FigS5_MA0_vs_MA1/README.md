# FigS5_MA0_vs_MA1

## Plotted parameters
Method: MA(0) vs MA(1) (1D/2D/3D). eta0=0.001; (1D) lambda=0.2,Omega=0.75t; (2D) lambda=0.25,Omega=0.5t; (3D) lambda=0.3,Omega=0.5t.
Grid spacing `dw ~ eta0/5`.

## Files in each panel folder
- `spectral_A_k0_MA0*` and `spectral_A_k0_MA1*` (csv/txt) -- the MA(0) and MA(1) curves, each `omega/t` vs `A(omega,k)` with one column per T.
- `self_energy_k0_MA0*` / `_MA1*` -- corresponding Re/Im Sigma.
- `*.pkl` -- the source pickles (`MA0_*` and `MA1_*` filenames).

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
- **Panel (1D)**: Omega=0.75 t, lambda=0.2, eta0=0.001 -- MA(0) & MA(1), T/Omega = 0.001, 0.267, 0.400, 0.667 (files tagged `_MA0`/`_MA1`).
- **Panel (2D)**: Omega=0.5 t, lambda=0.25, eta0=0.001 -- MA(0) & MA(1), T/Omega = 0.000, 0.200, 0.400, 0.600, 1.000 (files tagged `_MA0`/`_MA1`).
- **Panel (3D)**: Omega=0.5 t, lambda=0.3, eta0=0.001 -- MA(0) & MA(1), T/Omega = 0.200, 0.500, 0.600, 0.700, 0.800, 1.000 (files tagged `_MA0`/`_MA1`).


---
*Part of the data repository for the manuscript; see the top-level `README.md` and
`DATA_AVAILABILITY.md`.*


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
