
In the MA⁽¹⁾ and MA⁽0⁾ codes, the algorithm does not change with dimension except for the g0 propagator functions (and the dispersion `ε_k'):

| 1D | 2D | 3D |
 Coupling `g = √(λ·2D·t·Ω)` | `√(2λtΩ)` | `√(4λtΩ)` | `√(6λtΩ)` |
`ε_k = −2t Σᵧ cos(kᵧ)` | 1 cosine | 2 cosines | 3 cosines |

The dimensionless coupling is `λ = g²/(2Dt·Ω)`


For D>1, the local (momentum-averaged) free propagator `ḡ₀(ω)` is numerically solved:

elliptic `K` (AGM) | `∫dk_z ν K(ν)` (quadrature + AGM)



#  2D `ḡ₀(ω)` is complete elliptic integral `K`, evaluated by the AGM

$$\bar g_0^{\,\rm 2D}(\omega)=\frac{2}{\pi(\omega+i\eta)}\,\mathcal K\!\left(\frac{4t}{\omega+i\eta}\right),\qquad
\mathcal K(k)=\int_0^{\pi/2}\frac{d\phi}{\sqrt{1-k^2\cos^2\phi}} .$$

`K(k)` is the complete elliptic integral of the first kind.
It is evaluated by the **arithmetic–geometric mean (AGM)** —:
$$\mathcal K(k)=\frac{\pi}{2\,\operatorname{AGM}\!\bigl(1,\sqrt{1-k^2}\bigr)} .$$

Sample Code snippet (`G0_loc` for 2D case):

```python
z = omega                      # complex, ω + iη
k = (4.0*t) / z                # elliptic modulus
a = 1.0 + 0j
b = np.sqrt(1.0 - k*k)         # b0 = sqrt(1-k^2), principal branch
for _ in range(100):           # AGM iteration (converges in ~5–7 steps)
    c = (a + b)*0.5
    b = np.sqrt(a*b)
    a = c
    if np.abs(a - b) < _AGM_TOL:   # _AGM_TOL = 1e-14 (typical)
        break
K = np.pi / (2.0*a)
return (2.0 / (np.pi*z)) * K
```

A quick check is by doing the Brillouin-zone sum `ḡ₀(z)=N⁻²Σ_k 1/(z−ε_k)`


### 3D `ḡ₀(ω)` is a Gauss–Chebyshev quadrature over `k_z` of the 3D propagator

$$\bar g_0^{\,\rm 3D}(\omega)=\frac{1}{2\pi^2 t}\int_0^{\pi}\!dk_z\;\nu\,\mathcal K(\nu),
\qquad \nu=\frac{4t}{\omega+2t\cos k_z+i\eta}
= \frac1\pi\int_0^\pi \bar g_0^{\,\rm 2D}(\omega+2t\cos k_z)\,dk_z .$$

The `k_z` integral is done by **Gauss–Chebyshev quadrature** in `x = cos k_z`,

$$\int_0^\pi f(\cos k_z)\,dk_z=\int_{-1}^{1}\frac{f(x)}{\sqrt{1-x^2}}\,dx
\approx\frac{\pi}{N}\sum_{j=1}^{N} f(x_j),\qquad
x_j=\cos\!\frac{(2j-1)\pi}{2N},$$

so `(1/2π²t)·(π/N) = 1/(2π t N)`. For each node `x_j` the inner `K(ν_j)` is again
the AGM.

Sample Code snippet (`G0_loc` for 3D case):

```python
N = x_nodes.size
s = z + 2.0*t*x_nodes
val = 0.0 + 0.0j
for j in range(N):
    nu = (4.0*t) / s[j]
    K  = _ellipK_agm(nu)          # AGM, as in 2D
    val += nu * K
return (1.0 / (2.0*np.pi*t*N)) * val
```
```python
def _ellipK_agm(k):
    a = 1.0 + 0.0j
    b = np.sqrt(1.0 - k * k)
    for _ in range(100):
        an = 0.5 * (a + b)
        bn = np.sqrt(a * b)
        if (an.real - bn.real)**2 + (an.imag - bn.imag)**2 < _AGM_TOL:
            a = an
            break
        a, b = an, bn
    return np.pi / (2.0 * a)
```

Note: accuracy of `Ncheb ∝ 1/η` so empirically, we found that for eta<0.01, Ncheb>500

