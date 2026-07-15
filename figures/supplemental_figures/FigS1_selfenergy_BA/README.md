# FigS1_selfenergy_BA

## Plotted parameters
Method: Finite-T Born approximation (1D/2D/3D). eta0=0.001; (1D) lambda=0.5,Omega=2.5; (2D) lambda=0.75,Omega=4.5; (3D) lambda=0.75,Omega=6.25.
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
- **Panel (1D)**: Omega=2.5 t, lambda=0.5, eta0=0.001
  - Temperatures (T/Omega): 0.000, 0.120, 0.200, 0.400
  - omega grid: wmin=-8.0000 t, wmax=5.9995 t, dw=0.00050 t, N=28000
- **Panel (2D)**: Omega=4.5 t, lambda=0.75, eta0=0.001
  - Temperatures (T/Omega): 0.000, 0.222, 0.667
  - omega grid: wmin=-12.0000 t, wmax=11.9995 t, dw=0.00050 t, N=48000
- **Panel (3D)**: Omega=6.25 t, lambda=0.75, eta0=0.001
  - Temperatures (T/Omega): 0.000, 0.480, 0.800
  - omega grid: wmin=-16.0000 t, wmax=13.9995 t, dw=0.00050 t, N=60000



# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
