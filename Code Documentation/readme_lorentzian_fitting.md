

Walkthrough of the algorithm for  the multi-Lorentzian fitter

For small temperature steps `δT`, the spectrum evolves **continuously**. So the
best estimate for the fit at temperature `T` is simply the result
from the previous (slightly lower) temperature. 

---

## Step 1a — Load the specific file

```python
pkl_files = sorted(parent_dir.glob("MA1_1D_T*_k0.000_*.pkl"))
...
entries.sort(key=lambda x: x[0])   # sort by temperature T
```

The fitter scans one parameter folder (fixed `λ, Ω, η₀`) for the per-`T` pickles
produced by the MA⁽¹⁾ code (each holds `omega_vals` and `A_spectral`), and sorts
them by temperature. `λ, Ω, η₀` are read from the first pickle’s `params`.

Two module-level knobs control the sweep:
- `T_cutoff = 0.450` — stop fitting above this `T` 
- `offset = 600` — added on each side of the search window
  (see Step 2). Because `dw = η/5`, 600 points ≈ `120·η` in energy — this widens the
  fit window well to capture the thermal features relevant to the QP peal.

---

## Step 1b — Baseline fit at the lowest `T` (`≈0`): one Lorentzian

Manuscript step (i): *“identify the lowest-energy feature as the qp peak; fit a
single Lorentzian; record `E_P`, `Z_{k=0}`, `η₀`.”*

```python
E0_guess, idx0 = find_k0_leftmost_peak(omega0, A0)   # leftmost local maximum
...
lor1_simple = LorentzianModel(prefix="p1_")
params0["p1_center"].set(value=prev_peak_position)
params0["p1_sigma"].set(value=prev_w)                # seed width = η₀
result0 = model_simple.fit(A_fit0, params0, x=omega_fit0, method="least_squares")
```

- `find_k0_leftmost_peak` returns the **smallest-ω local maximum** — at `T≈0` the
  polaron ground state is the lowest-energy feature, so “leftmost peak” = *qp* peak.
 )
- A **single** `LorentzianModel` (LMFIT) is fit around it
- The fitted amplitude / center / width become the seeds `prev_A`, `prev_peak_position`,
  `prev_w` for the first `T>0` step. LMFIT’s `LorentzianModel` parametrises the peak
  as `A/π · σ/((ω−μ)² + σ²)`, so the **amplitude parameter is the area = the *qp*
  weight `Z`** and `σ` is the half-width at half-maximum = `η`.

---

## Step 2 — For each `T > 0`: a windowed 4-Lorentzian fit

### 2a. Build the search window (manuscript step (ii))

```python
left_i, right_i = build_window(omega, prev_peak_position, halfwidth=0.25)
left_i  = left_i  - offset
right_i = right_i + offset
```

A window of half-width `~0.25 t` (then padded by `offset` grid points) is centred on
the previous-`T` peak position — 

### 2b. qp + 3 thermal Lorentzians

```python
lor1 = LorentzianModel(prefix="p1_")   # the qp peak
lor2 = LorentzianModel(prefix="p2_")   # thermal feature (just above)
lor3 = LorentzianModel(prefix="p3_")   # thermal feature (below)
lor4 = LorentzianModel(prefix="p4_")   # thermal feature (further above)
model = lor1 + lor2 + lor3 + lor4
```


### 2c. Warm start + physical constraints (the heart of the method)

Every parameter is **seeded from the previous `T`** and **bounded** so the fit stays
physical and the *qp* peak cannot swap identity with a thermal sideband:

**qp peak `p1` — amplitude (weight) monotonically bounded:**
```python

    params["p1_amplitude"].set(value=prev_A, min=0.3*prev_A, max=1.5*prev_A)

```

**qp peak `p1` — position pinned near the previous peak:**
```python
params["p1_center"].set(value=prev_peak_position,
                        min=prev_peak_position-0.05, max=prev_peak_position+0.1)
```

**qp peak `p1` — width can only grow:**
```python
params["p1_sigma"].set(value=prev_w, min=0.75*prev_w, max=3.0*prev_w)
```

Thermal peaks `p2,p3,p4`  Their centres are
offsets from `p1_center` (two above, one below), constrained to stay inside the
window:
```python
params.add("deltaE2", value= 0.025, min= 0.005,        max= width_in_w)
params.add("deltaE3", value=-0.05,  min=-width_in_w,   max=-0.025)
params.add("deltaE4", value= 0.1,   min= 0.05,         max= width_in_w)
params["p2_center"].set(expr="p1_center + deltaE2")
params["p3_center"].set(expr="p1_center + deltaE3")
params["p4_center"].set(expr="p1_center + deltaE4")
```
and their widths are forced to be broader than the *qp* peak (`≥ 1.25·σ_qp`),
implementing the manuscript’s constraint “*thermal features are wider than the qp
peak*”:
```python
params.add("w2_factor", value=10.0, min=1.25, max=500.0)   # ×σ_qp
params.add("w3_factor", value=20.0, min=1.25, max=500.0)
params.add("w4_factor", value= 5.0, min=1.25, max=500.0)
params["p2_sigma"].set(expr="w2_factor * p1_sigma")
...
```
Amplitudes of the thermal peaks are capped at `0.5·prev_A`  Using LMFIT `expr=` ties these as constrained parameters.

### 2d. Fit and score

```python
result = model.fit(A_fit, params, x=omega_fit,
                   method="least_squares", nan_policy="omit", max_nfev=50000)
```
Non-linear least squares (Levenberg–Marquardt / TRF via LMFIT). Then an **`R²`** is
computed against the summed model:
```python
Lsum = L1 + L2 + L3 + L4
R2 = 1 - ss_res/ss_tot
```
This is the manuscript’s goodness-of-fit metric (`R² > 0.99` is one of the three
confidence criteria.

### 2e. Record and march

The *qp* row `(k, Z=A1, η*=w1, E_P=E1, R², errors…)` is written to a per-`T` table,
a diagnostic figure is saved, and crucially the converged *qp* parameters seed the
next temperature:
```python
prev_A = A1; prev_w = w1; prev_peak_position = E1
```

---
