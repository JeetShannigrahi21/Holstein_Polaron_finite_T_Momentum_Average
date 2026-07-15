# FigEM2_1D_continuum_k

## Plotted parameters
Method: MA(1) (1D). 1D, Omega=2t, lambda=1, eta0=0.005; T=0.001,0.3,0.5; k/pi from 0 to 0.5.
Grid spacing `dw ~ eta0/5`.

## Files in each panel folder
- `spectral_A_<MA0|MA1>_kpi<k/pi>.csv` / `.txt` -- for each momentum `k/pi`, column 1 is `omega/t` and each further column is `A(omega,k)` at one temperature.
- `self_energy_<...>_kpi<k/pi>.csv` -- corresponding Re/Im Sigma when present.
- `*.pkl` -- one source pickle per (temperature, momentum).

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
- **Panel (Om2.0_lam1.0)**: Omega=2 t, lambda=1, eta0=0.005 -- MA1; k/pi = 0.000, 0.056, 0.111, 0.167, 0.222, 0.278, 0.333, 0.389, 0.444, 0.500; T = 0.001, 0.3, 0.5.


---
*Part of the data repository for the manuscript; see the top-level `README.md` and
`DATA_AVAILABILITY.md`.*


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
