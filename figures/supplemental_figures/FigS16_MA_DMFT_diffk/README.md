# FigS16_MA_DMFT_diffk

## Plotted parameters
Method: MA(0) & MA(1) (1D). 1D, lambda=0.01, Omega=1.0t, eta0=0.05; k/pi = 0, 1/3, 2/3, 1.
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
- **Panel (Om1.0_lam0.01)**: Omega=1 t, lambda=0.01, eta0=0.05 -- MA0 & MA1; k/pi = 0.000, 0.333, 0.667, 1.000; T = 1, 3, 4, 5, 8.


## Note
**External data not included.** The published figure also overlays numerically-exact results from other groups (DMFT). Those curves are the property of their original authors and are available from the cited references -- they are NOT redistributed here. Only our Momentum-Average curves are provided; they are reproducible from the MA code in `Code Documentation/` at the parameters above.


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
