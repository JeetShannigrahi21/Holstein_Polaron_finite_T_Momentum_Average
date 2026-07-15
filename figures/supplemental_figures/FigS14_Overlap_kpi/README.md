# FigS14_Overlap_kpi

## Plotted parameters
Method: MA(0) & MA(1) (1D). 1D, lambda=1, Omega=t=1, eta0=0.05, T=0.4 Omega, k=pi.
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
- **Panel (Om1.0_lam1.0_kpi)**: Omega=1 t, lambda=1, eta0=0.05 -- MA(0) & MA(1) at k/pi=1.000, T/Omega = 0.400 (files tagged `_MA0`/`_MA1`).


## Note
**External data not included.** The published figure also overlays numerically-exact results from other groups (VED-FTLM, finite-T DMRG, DMFT). Those curves are the property of their original authors and are available from the cited references -- they are NOT redistributed here. Only our Momentum-Average curves are provided; they are reproducible from the MA code in `Code Documentation/` at the parameters above.

---
*Part of the data repository for the manuscript; see the top-level `README.md` and
`DATA_AVAILABILITY.md`.*


# Data licence

Unless otherwise stated, the original research data in this directory are
licensed under the Creative Commons Attribution 4.0 International License.

SPDX-FileCopyrightText: 2026 [JEET SHANNIGRAHI]
SPDX-License-Identifier: CC-BY-4.0

See `../../../LICENSES/CC-BY-4.0.txt`.
