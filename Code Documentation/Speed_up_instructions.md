
For MA1, the 2D/3D self-energy is expensive because each frequency evaluation
`Σ̃(ω₀)` calls `ḡ₀` thousands of times (across `compute_A_of_n`, `a_2`, `b_1/b_2`,
`F₁`, and the level-1 renormalised branches, for every `n_l` in the thermal sum).

Hence, several optimisation steps can be taken taken:

### pure Numba func tions

In every class there are pure functions, taking
all inputs explicitly (`omega, g, Omega, t, n_max, weights, [x_nodes,] M,
thermal_cutoff`). They are therefore compiled once
at import.
The frequency sweep is one `@njit(parallel=True)` kernel:

```python
@njit(parallel=True, fastmath=True)
def sigma_tilde_all(omega_arr, ...):
    out = np.empty(omega_arr.shape, dtype=np.complex128)
    for i in prange(omega_arr.size):        # frequencies are independent
        out[i] = Sigma_tilde(omega_arr[i], ...)
    return out
```


### In 2D and 3D, `ḡ₀(ω₀+jΩ)` memoization 

Within one `Σ̃(ω₀)` evaluation, every `ḡ₀` call lands on
the integer grid `ω₀ + jΩ` so the grid is built and then called:

```python
@njit(...)
def Sigma_tilde(omega, ...):
    w0 = omega
    j0 = M + 2
    n_grid = M + n_max + 5
    g0g = np.empty(n_grid, dtype=np.complex128)
    for idx in range(n_grid):                        # build g0 grid ONCE
        g0g[idx] = G0_loc(w0 + (idx - j0)*Omega, ...)
    xi = xi_tilde(omega, ..., w0, g0g, j0)
    return xi / (1.0 + g0g[j0]*xi)                   # g0g[j0] == G0_loc(ω₀)

@njit(...)
def g0_at(arg, w0, Omega, ..., g0g, j0):             # memoized lookup
    j   = int(np.rint(((arg - w0)/Omega).real))
    idx = j + j0
    if 0 <= idx < g0g.size and abs(arg - (w0 + j*Omega)) < 1e-6:
        return g0g[idx]                              # cache hit
    return G0_loc(arg, ...)                          # fallback
```

`g0_at` **verifies** that its argument really equals `ω₀+jΩ` to a tight complex
tolerance before returning the cached value, and otherwise falls back to a direct
`G0_loc`. 


## Typical python environment

| Package | Version tested | Role |
|---|---|---|
| Python | 3.12.11 | — |
| NumPy | 2.4.1 | arrays, complex `sqrt` (principal branch) |
| Numba | 0.64.0 | `@njit` kernels, `prange`, `cache=True` |
| matplotlib | 3.10.6 | spectral-function PNGs |

