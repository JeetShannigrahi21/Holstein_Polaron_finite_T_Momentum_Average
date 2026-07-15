# FigS17_MA_VED



## Plotted parameters
Method: MA(0) & MA(1) (1D). 1D, lambda=1, Omega=0.75t, eta0=0.01, k=0.
Grid spacing `dw ~ eta0/5`.

VED data is also attached.

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
- **Panel (Om0.75_lam1.0_k0)**: Omega=0.75 t, lambda=1, eta0=0.01 -- MA(0) & MA(1) at k/pi=0.000, T/Omega = 0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500 (files tagged `_MA0`/`_MA1`).




# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
