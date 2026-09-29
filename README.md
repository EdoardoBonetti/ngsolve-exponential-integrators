# Exponential integrators in NGSolve

A four-part tutorial series on exponential integrators for time-dependent finite element
problems, written in the style of the NGSolve i-tutorials (section 3, time stepping).
Everything is pure Python on top of the public NGSolve API — no changes to the C++ core.

| Part | Notebook | Content | runtime |
|---|---|---|---|
| 1 | [`01_heat_exponential_euler/expint_heat.ipynb`](01_heat_exponential_euler/expint_heat.ipynb) | Heat equation; exact step `u_{n+1} = e^{-dt A} u_n + dt φ₁(-dt A) M⁻¹f`; Lanczos in the mass-matrix inner product; polynomial vs. **shift-and-invert** Krylov; `KrylovExp` as a `BaseMatrix`; order study IE / CN / exponential Euler; tests | ~10 s |
| 2 | [`02_matrix_exponential_methods/matrix_functions.ipynb`](02_matrix_exponential_methods/matrix_functions.ipynb) | How to compute `e^{-tA}v` for a large sparse FE operator: polynomial Lanczos (Hochbruck–Lubich bound, Saad estimate), `scipy.sparse.linalg.expm_multiply`, Chebyshev expansion, shift-and-invert Lanczos (choice of γ, inexact solves), **contour integrals** with complex shifts, augmented-matrix trick, timing comparison | ~20 s |
| 3 | [`03_convection_diffusion_and_sources/convdiff_expRK.ipynb`](03_convection_diffusion_and_sources/convdiff_expRK.ipynb) | Non-symmetric operators (Arnoldi, Hessenberg matrix, field of values); time-dependent sources: exponential Euler and exponential trapezoidal rule (φ₂), order study | ~40 s |
| 4 | [`04_nonlinear_allen_cahn/allen_cahn_exprb.ipynb`](04_nonlinear_allen_cahn/allen_cahn_exprb.ipynb) | Semilinear Allen–Cahn: exponential Euler, exponential Rosenbrock–Euler, IMEX Euler; energy decay, order study, large steps | ~15 s |

Supporting files:

* [`expint_tools.py`](expint_tools.py) — the shared library: `phi`, `krylov_funm`, `KrylovExp`,
  `ContourExp`, `chebyshev_exp`, `lanczos_spectral_bound`, `DenseReference`. Part 1 develops the
  core routines inline; Parts 2–4 import them.
* [`tests/test_expint.py`](tests/test_expint.py) — pytest suite (11 tests, ~3 s) checking every
  method against dense references and the orders of the time stepping schemes.
* `old/` — the original exploratory notebooks (kept unchanged for reference; their exponential
  parts contain known bugs that the new notebooks fix).
* `_toc.yml`, `_config.yml` — minimal [Jupyter Book](https://jupyterbook.org) configuration.

## Running

The notebooks need NGSolve with `webgui_jupyter_widgets`, plus numpy, scipy and matplotlib.
On this machine NGSolve is the source build installed in `/Applications/Netgen.app`; either
select the Jupyter kernel **"Python 3 (NGSolve, Netgen.app)"** (registered in
`~/Library/Jupyter/kernels/ngsolve-netgen`) or set the path by hand:

```bash
export PYTHONPATH=/Applications/Netgen.app/Contents/Resources/lib/python3.13/site-packages
```

Headless execution of a notebook (run inside its folder so that `expint_tools` is found):

```bash
cd 01_heat_exponential_euler && python3 -m jupyter nbconvert --to notebook --execute expint_heat.ipynb --output /tmp/out.ipynb
```

Tests:

```bash
python3 -m pytest tests -q
```

Jupyter Book:

```bash
pip install jupyter-book && jupyter-book build .
```

## The methods in one table

For the semi-discrete problem `M u' = -K u + f`, `A = M⁻¹K` (self-adjoint in the `M`-inner
product, spectrum in `[λ_min, λ_max]`, `λ_max ~ h⁻²`), and a target tolerance `ε`:

| method | needs | work per application of `e^{-dt A}` | mesh dependent? |
|---|---|---|---|
| polynomial Lanczos | products with `A` (= one mass solve each) | `m ≈ √(dt λ_max) + O(log 1/ε)` | yes |
| truncated Taylor (`expm_multiply`) | products with `A` | `∝ dt λ_max` | yes |
| Chebyshev expansion | products with `A`, bound for `λ_max` | `≈ dt λ_max / 2 + O(log 1/ε)` | yes |
| **shift-and-invert Lanczos**, `γ ≈ dt/10` | one factorisation of `M + γK` | 10–30 back-substitutions | **no** |
| **contour integral** (parabolic, N points) | N/2 complex factorisations of `z_k M + K` | N/2 back-substitutions, parallel | **no** |

`φ_k` functions come from the same machinery with a different scalar function (Krylov) or, for the
contour method, from the recursion `φ_k(-dtA) = -(dtA)⁻¹(φ_{k-1}(-dtA) - I/(k-1)!)`.

## Pitfalls (all encountered while writing this)

* `from ngsolve import *` exports `exp`, `sin`, `sqrt`, `x`, `y`, `z`: never call a vector `y`;
  use `np.exp` on numpy arrays.
* numpy scalars (`np.float64`) do not multiply NGSolve vectors — wrap them in `float(...)`.
* `mat.COO()` exports only the lower triangle of a form assembled with `symmetric=True`; assemble
  with `symmetric=False` when exporting to scipy.
* Krylov start vectors must be zero on the Dirichlet dofs (`Projector(freedofs, True)`), otherwise
  the `M`-inner product couples them to the boundary and the iteration diverges.
* Evaluate functions of the small projected matrix through its eigendecomposition (or the
  augmented matrix), never through `inv(T)`.
* Complex shifts require the matrices on a `complex=True` space; use `umfpack` for the solves.
* A bare `E * vec` is a lazy expression in NGSolve: call `.Evaluate()` (or assign to `.data`)
  before reading `E.info`.
* The right-hand side of an inner CG solve must be projected onto the free dofs.

## Submitting to the NGSolve i-tutorials

The notebooks follow the conventions of `docs/i-tutorials/unit-3.1-parabolic/parabolic.ipynb`
(`from ngsolve import *`, `webgui` `Draw`, `mstar.AsVector()` linear combinations, multidim
animation). To add Part 1 as unit 3.9: copy `expint_heat.ipynb` and `expint_tools.py` to
`docs/i-tutorials/unit-3.9-expint/`, and add
`* [3.9](unit-3.9-expint/expint_heat.ipynb) Exponential integrators via Krylov methods` to
`docs/i-tutorials/index.ipynb` and `unit-3.9-expint/expint_heat.ipynb` to `index.rst`.
`nbsphinx` executes the notebooks at build time with `allow_errors = False`, so the assertions in
the test cells act as CI.

## References

* Y. Saad, *Analysis of some Krylov subspace approximations to the matrix exponential operator*, SIAM J. Numer. Anal. 29 (1992). doi:10.1137/0729014
* M. Hochbruck, C. Lubich, *On Krylov subspace approximations to the matrix exponential operator*, SIAM J. Numer. Anal. 34 (1997). doi:10.1137/S0036142995280572
* J. van den Eshof, M. Hochbruck, *Preconditioning Lanczos approximations to the matrix exponential*, SIAM J. Sci. Comput. 27 (2006). doi:10.1137/040605461
* I. Moret, P. Novati, *RD-rational approximations of the matrix exponential*, BIT 44 (2004). doi:10.1023/B:BITN.0000046805.27551.3b
* M. Hochbruck, A. Ostermann, *Exponential integrators*, Acta Numerica 19 (2010). doi:10.1017/S0962492910000048
* M. Hochbruck, A. Ostermann, J. Schweitzer, *Exponential Rosenbrock-type methods*, SIAM J. Numer. Anal. 47 (2009). doi:10.1137/080717717
* A. H. Al-Mohy, N. J. Higham, *Computing the action of the matrix exponential*, SIAM J. Sci. Comput. 33 (2011). doi:10.1137/100788860
* L. N. Trefethen, J. A. C. Weideman, T. Schmelzer, *Talbot quadratures and rational approximations*, BIT 46 (2006). doi:10.1007/s10543-006-0077-9
* J. A. C. Weideman, L. N. Trefethen, *Parabolic and hyperbolic contours for computing the Bromwich integral*, Math. Comp. 76 (2007). doi:10.1090/S0025-5718-07-01945-X
* S. Güttel, *Rational Krylov approximation of matrix functions*, GAMM-Mitt. 36 (2013). doi:10.1002/gamm.201310002
* S. Gaudreault, G. Rainwater, M. Tokman, *KIOPS: A fast adaptive Krylov subspace solver for exponential integrators*, J. Comput. Phys. 372 (2018). doi:10.1016/j.jcp.2018.06.026
