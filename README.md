# Data repository for the finite-temperature Holstein polaron (through the Momentum Average)

> **The effective mass and lifetime of single Holstein polarons at finite temperatures**
> J. Shannigrahi, J. Bončа, M. Berciu

This repository holds the numerical data behind the figures of the manuscript and
its Supplemental Material, generated with the finite-temperature Momentum Average
(MA⁽⁰⁾/MA⁽¹⁾) approximation in both the main text and the supplemental material. 

It is intended to be self-contained and FAIR-compliant. Data is in text format + the original pickles + csv and every figure has a readme file for added ease of acess, 

## License

See `LICENSE.md` for details. Full legal texts are in `LICENSES/`.

- Data, figures, documentation:
  CC BY 4.0 (`LICENSES/CC-BY-4.0.txt`)

- Python codes in "Code Documentation":
  BSD 3-Clause License (`LICENSES/BSD-3-Clause.txt`)

## Layout

```
Data_repository_for_paper/
├── README.md                  ← this file
├── LICENSE.md                ← BSD-3 for codes and CC-BY-4 for plots/data
├── LICENSES/                 ← full legal texts (BSD-3-Clause.txt, CC-BY-4.0.txt)
└── figures/
    ├── main_text_figures/     ← figures that appear in the main Letter (+ End Matter)
    │   └── <FigName>/
    │       ├── README.md       ← PUBLIC per-figure doc: what it shows, params, how to read the files
    │       └── panel_<...>/    ← one folder per parameter set (Ω, λ, η₀) / dimension / momentum
    │           ├── spectral_A_*.csv / .txt   ← ω and A(ω,k) for each plotted T
    │           ├── self_energy_*.csv          ← ω, Re/Im Σ per T (where relevant)
    │           └── *.pkl                       ← the source MA pickle(s), IN THE SAME FOLDER
    ├── supplemental_figures/  ← figures that appear in the Supplemental Material
    │   └── <FigName>/ …        (same panel layout)
    └── fitted plots/          ← Lorentzian-fit inputs for every m*/η* curve (Main text Fig 3, S12, S13)
        ├── main_text/  &  supplemental/
        │   └── MA1_<dim>_Omega…_lam…_eta…/
        │       ├── pickle data/    ← per-T A(ω,k=0) pickles 
        │       └── fitted data/     ← combined gs-vs-T table + individual fit PNGs
```




**Main text** (`figures/main_text_figures/`):

| Figure folder | Paper | Contents |
|---|---|---|
| `Fig01_1D_benchmark_k0` | Main Fig. 1 | MA⁰ & MA¹ A(ω,k=0), T=0.4Ω (
| `Fig02_3D_spectral_grid` | Main Fig. 2 (3×3 grid) | , 9 param sets, Ω∈{0.5,1,2}×λ∈{0.5,1,1.5} |
| `Fig03_eff_mass_lifetime` | Main Fig. 3 | m*/m₀ and η\* vs T (1D/2D/3D), Ω=2t |
| `Fig05_1D_continuum_k` | End Matter | k-resolved MA¹ A(ω,k), 0≤k≤π/2, T=0.001/0.3/0.5 |

**Supplemental** (`figures/supplemental_figures/`):


| Figure folder | Paper | Contents |
|---|---|---|
| `FigS1_selfenergy_BA` | SM Fig. S1 | Born-approx A & Im Σ (1D/2D/3D) |
| `FigS3_selfenergy_MA1` | SM Fig. S3 |  MA¹ A & Im Σ (1D/2D/3D) |
| `FigS4_selfenergy_MA0` | SM Fig. S4 | MA⁰ A & Im Σ (1D/2D/3D) |
| `FigS5_MA0_vs_MA1` | SM Fig. S5 |  MA⁰ vs MA¹ overlay (both methods) |
| `FigS6_1D_spectral_matrix` | SM Fig. S6 (fig:1D_Akw) |  1D 3×3 grid (Ω×λ) — diff-Ω × diff-λ matrix |
| `FigS7_2D_spectral_matrix` | SM Fig. S7 (fig:2D_Akw) |  2D 3×3 grid (Ω×λ) |
| `FigS8_heatmap_1D_Om0.5` / `FigS9_heatmap_1D_Om2.0` | SM Figs. S8–S9 | A(ω,k) density maps (matrices in pickles) |
| `FigS10_m_star_fitting` | SM Fig. S10 | m*/m₀ vs T (4 panels) + quadratic-in-n_B fit params |
| `FigS11_eta_star_fitting` | SM Fig. S11 |  η\* vs T (4 panels) + fit params |
| `FigS12_eff_mass_lifetime_Om1.0` | SM Fig. S12 |m*/m₀ and η\* vs T (1D/2D/3D), Ω=1t |
| `FigS13_eff_mass_lifetime_Om0.75` | SM Fig. S13 |  m*/m₀ and η\* vs T (1D/2D/3D), Ω=0.75t |
| `FigS14_Overlap_kpi` | SM Fig. S14 | MA⁰ & MA¹ A(ω,k=π), T=0.4Ω (MA-only) |
| `FigS15_MA_DMFT_selfenergy` | SM Fig. S15 | MA⁰ & MA¹ vs DMFT — MA-only |
| `FigS16_MA_DMFT_diffk` | SM Fig. S16 | MA⁰ & MA¹ A(ω,k) at k=0,π/3,2π/3,π — MA-only |
| `FigS17_MA_VED` | SM Fig. S17 | MA⁰ & MA¹ vs VED-FTLM — MA-only |
| `FigS18_VED_DMFT_MA` | SM Fig. S18 | MA⁰ & MA¹ vs VED-FTLM+DMFT — MA-only |

**`fitted plots/`** contains, for Figs. 3, S12 and S13 the underlying per-temperature spectra (`pickle data/`) and their individual multi-Lorentzian fits (`fitted data/`: the combined `gs_data_vs_T…` table + the `fig_fit_T*.png` fit images).
Folder names are `MA1_<dim>_Omega…_lam…_eta…`

**External data policy.** Six benchmarking figures (`Fig01`, `FigS14_Overlap_kpi`,
`FigS15_MA_DMFT_selfenergy`, `FigS16_MA_DMFT_diffk`, `FigS17_MA_VED`, `FigS18_VED_DMFT_MA`)
are shown in the paper overlaid with **external** VED-FTLM / finite-T DMRG / DMFT
curves that were shared privately with the authors. Please reach out to the original authors for the data.

## File formats & column convention

| Format | Purpose |
|---|---|
| `.csv` | primary, comma-separated, one header row (UTF-8) |
| `.txt` | same numbers, tab-delimited |
| `.pkl` | full MA object (Python pickle) — **MA data only** |

Column 1 is always `omega_over_t` (ω/t). Spectral columns are headed
`A_T<T>_ToverOmega<T/Ω>`; self-energy columns `ReSigma_T<T>`, `ImSigma_T<T>`.
**Temperature `T` is stored in units of `t`**; figures label curves by `T/Ω` — both
appear in every header. The CSV/TXT hold the **raw** A(ω);


## Code documentation is in "\Code Documentation"

It contains the MA0 and MA1 python codes for the 1D case. There is an attached readme.md file explaining it. Futhermore, there is another one detailing the changes needed for the 2D and 3D cases (g0_propagators_2D_3D.md) and for optimising the code: "Speed_up_instructions.py"

The fits obtained on the various Lorentzians (m* and eta*) was done through "Multi_lorentzian_fitting.py", explained through "readme_lorentzian_fitting.md"
