"""
expint_tools.py -- building blocks for exponential integrators in NGSolve
=========================================================================

Everything here is plain Python on top of the public NGSolve API; no C++ is needed.
The functions are developed step by step in the notebooks 01 and 02 and collected
here so that notebooks 03 and 04 can import them.

Notation (finite-element semidiscretisation of a parabolic problem):

    M u'(t) = -K u(t) + f        ->      u' = -A u + M^{-1} f,   A = M^{-1} K

A is self-adjoint w.r.t. the M-inner product (u,v)_M = u^T M v.  All Krylov spaces
below are therefore built with M-orthonormal bases, and all norms are M-norms
(i.e. L2 norms of the finite-element functions).

Pitfalls (all of them bit us while writing this):
  * `from ngsolve import *` exports exp, sin, sqrt, x, y, z -- do not call a vector `y`,
    and use np.exp on numpy arrays.
  * numpy scalars do not multiply NGSolve vectors: wrap them in float(...).
  * mat.COO() returns only the lower triangle if the form was assembled with symmetric=True.
  * Krylov start vectors must live on the free dofs (use Projector(freedofs, True)).
  * Evaluate functions of the small projected matrix via an eigendecomposition, never via inv().
"""

from math import sqrt, factorial
import numpy as np
import scipy.linalg as sla
import scipy.sparse as sp
import scipy.special as spec

from ngsolve import BaseMatrix, BaseVector, MultiVector, InnerProduct, Projector, Vector


# ----------------------------------------------------------------------------------
# scalar phi-functions
# ----------------------------------------------------------------------------------

def phi(k, z):
    """phi_k(z) for numpy arrays (real or complex), stable near z = 0.

    phi_0(z) = e^z,   phi_{k+1}(z) = (phi_k(z) - 1/k!) / z,
    i.e. phi_1(z) = (e^z - 1)/z,  phi_2(z) = (e^z - 1 - z)/z^2, ...
    For |z| < 0.5 the Taylor series sum_j z^j/(j+k)! is used (20 terms, error < 1e-18);
    z = +-inf is mapped to the correct limit (0 for -inf).
    """
    z = np.asarray(z)
    out = np.zeros(z.shape, dtype=np.result_type(z, float))
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        small = np.abs(z) < 0.5
        zs = z[small]
        s = np.zeros_like(zs, dtype=out.dtype)
        for j in range(19, -1, -1):          # Horner
            s = s * zs + 1.0 / factorial(j + k)
        out[small] = s
        zl = z[~small]
        p = np.exp(zl)
        for i in range(k):
            p = (p - 1.0 / factorial(i)) / zl
        out[~small] = p
    out = np.where(np.isfinite(out), out, 0.0)   # e.g. z = -inf
    return out


# ----------------------------------------------------------------------------------
# functions of the small projected matrix
# ----------------------------------------------------------------------------------

def funm_small_sym(T, func):
    """func(T) e_1 for a small symmetric matrix T, via its eigendecomposition."""
    th, Q = sla.eigh(0.5 * (T + T.T))
    return Q @ (func(th) * Q[0, :])


def funm_small_gen(H, func):
    """func(H) e_1 for a small non-symmetric (Hessenberg) matrix H.

    Uses the eigendecomposition if it is well conditioned, otherwise the
    Schur-Parlett algorithm of scipy.linalg.funm.  Returns a real vector when H is real.
    """
    m = H.shape[0]
    e1 = np.zeros(m); e1[0] = 1.0
    th, Q = sla.eig(H)
    if np.linalg.cond(Q) < 1e8:
        res = Q @ (func(th) * sla.solve(Q, e1))
    else:
        res = sla.funm(H, func) @ e1
    return np.real(res) if np.isrealobj(H) else res


# ----------------------------------------------------------------------------------
# Krylov approximation of f(op) v in the M-inner product
# ----------------------------------------------------------------------------------

def krylov_funm(op, M, v, func, maxm=60, tol=1e-8, symmetric=True, info=None):
    """Approximate func(op) v by a Krylov method in the M-inner product.

    op        : callable BaseVector -> BaseVector (the operator, e.g. x -> M^{-1} K x
                or x -> (M + gamma K)^{-1} M x).  Must map free dofs to free dofs.
    M         : mass matrix defining the inner product (u,v)_M = u^T M v
    v         : start vector (BaseVector, supported on the free dofs)
    func      : vectorised scalar function, applied to the Ritz values of op
    maxm      : maximal Krylov dimension
    tol       : stop when the M-norm of the change of the approximation
                between two consecutive Krylov dimensions is below tol*||v||_M
    symmetric : True -> op is M-self-adjoint (Lanczos, eigh on T_m);
                False -> general (Arnoldi, eig on the Hessenberg matrix H_m)
    info      : optional dict, receives "m" (dimension used) and "hist" (estimates)

    Returns the approximation as a BaseVector.

    One column of the Arnoldi/Lanczos process is exactly what NGSolve's
    MultiVector.AppendOrthogonalize(w, ipmat=M) does: it M-orthogonalises w against
    the existing basis (two passes of modified Gram-Schmidt), appends the normalised
    remainder, and returns the coefficients h_{0..j+1}.
    """
    beta = sqrt(InnerProduct(v, M * v))
    if beta == 0.0:
        if info is not None:
            info["m"], info["hist"] = 0, []
        return (0.0 * v).Evaluate()

    V = MultiVector(v, 0)
    V.Append((1.0 / beta) * v)
    H = np.zeros((maxm + 1, maxm))
    Eold = np.zeros(0)
    hist = []
    for j in range(maxm):
        w = op(V[j])
        if not isinstance(w, BaseVector):
            w = w.Evaluate()
        h = np.array(V.AppendOrthogonalize(w, ipmat=M)).ravel()
        H[:j + 2, j] = h[:j + 2]
        Hm = H[:j + 1, :j + 1]
        E = beta * (funm_small_sym(Hm, func) if symmetric else funm_small_gen(Hm, func))
        diff = np.linalg.norm(E - np.append(Eold, np.zeros(j + 1 - len(Eold))))
        hist.append(diff)
        Eold = E
        if h[j + 1] < 1e-14 * abs(h).max():   # happy breakdown: Krylov space is invariant
            break
        if j >= 1 and diff < tol * beta:
            break
    m = len(E)
    if info is not None:
        info["m"], info["hist"] = m, hist
    return (V[0:m] * Vector(E)).Evaluate()


class KrylovExp(BaseMatrix):
    """y = f(-dt A) x  with  A = M^{-1} K  on the free dofs, via Krylov methods.

    poly=False (default): shift-and-invert Lanczos/Arnoldi on
            B = (M + gamma K)^{-1} M = (I + gamma A)^{-1},
        eigenvalues theta of B and lambda of A are related by lambda = (1/theta - 1)/gamma.
        One sparse factorisation of M + gamma K (once), m back-substitutions per apply.
        Convergence is independent of the mesh and of dt.  Default gamma = dt/10.
    poly=True: polynomial Lanczos/Arnoldi on A itself (needs ~ sqrt(dt*lambda_max) steps).

    Mult(x, y)     : y = exp(-dt A) x          (so `E * x` works like any NGSolve matrix)
    Phi(k, x)      : phi_k(-dt A) x
    Apply(x, func) : func(A) x for an arbitrary vectorised scalar func
    info           : dict with the Krylov dimension "m" and estimator history of the last apply
    """

    def __init__(self, M, K, dt, freedofs, gamma=None, tol=1e-8, maxm=60,
                 poly=False, symmetric=True, inverse=None):
        super().__init__()
        self.M, self.K, self.dt = M, K, dt
        self.tol, self.maxm, self.symmetric, self.poly = tol, maxm, symmetric, poly
        self.P = Projector(freedofs, True)
        self.info = {}
        self.tmp = M.CreateColVector()
        inv = inverse or ("sparsecholesky" if symmetric else "umfpack")
        if poly:
            self.gamma = None
            self.invM = M.Inverse(freedofs, inverse=inv)
            self.eigmap = lambda th: th
        else:
            self.gamma = 0.1 * dt if gamma is None else gamma
            mstar = M.CreateMatrix()
            mstar.AsVector().data = M.AsVector() + self.gamma * K.AsVector()
            self.invmstar = mstar.Inverse(freedofs, inverse=inv)
            g = self.gamma
            with np.errstate(divide="ignore"):
                self.eigmap = lambda th: np.where(np.real(th) > 0, (1.0 / th - 1.0) / g, np.inf)

    # --- BaseMatrix interface -------------------------------------------------------
    def Height(self): return self.M.height
    def Width(self): return self.M.width
    def IsComplex(self): return False
    def CreateRowVector(self): return self.M.CreateRowVector()
    def CreateColVector(self): return self.M.CreateColVector()

    # --- the operator handed to the Krylov process -------------------------------------
    def _op(self, xv):
        out = self.M.CreateColVector()
        if self.poly:
            self.tmp.data = self.K * xv
            out.data = self.invM * self.tmp
        else:
            self.tmp.data = self.M * xv
            out.data = self.invmstar * self.tmp
        return out

    # --- public methods --------------------------------------------------------------
    def Apply(self, x, func):
        """func(A) x, func vectorised scalar function of the eigenvalues lambda of A."""
        xp = self.M.CreateColVector()
        xp.data = self.P * x
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            return krylov_funm(self._op, self.M, xp, lambda th: func(self.eigmap(th)),
                               self.maxm, self.tol, self.symmetric, self.info)

    def Mult(self, x, y):
        y.data = self.Apply(x, lambda lam: np.exp(-self.dt * lam))

    def Phi(self, k, x):
        """phi_k(-dt A) x"""
        return self.Apply(x, lambda lam: phi(k, -self.dt * lam))


# ----------------------------------------------------------------------------------
# polynomial alternative: Chebyshev expansion (symmetric A, spectrum in [0, lam_max])
# ----------------------------------------------------------------------------------

def lanczos_spectral_bound(applyA, M, v, m=30):
    """Upper bound for lambda_max(A) from m Lanczos steps (A M-self-adjoint).

    Returns (theta_max + residual) * 1.05 where theta_max is the largest Ritz value and
    residual = |beta_{m+1} s_m| is the Ritz residual (which bounds the eigenvalue error).
    """
    beta = sqrt(InnerProduct(v, M * v))
    V = MultiVector(v, 0); V.Append((1.0 / beta) * v)
    T = np.zeros((m + 1, m))
    for j in range(m):
        w = applyA(V[j])
        if not isinstance(w, BaseVector):
            w = w.Evaluate()
        h = np.array(V.AppendOrthogonalize(w, ipmat=M)).ravel()
        T[:j + 2, j] = h[:j + 2]
    Tm = 0.5 * (T[:m, :m] + T[:m, :m].T)
    th, S = sla.eigh(Tm)
    resid = abs(T[m, m - 1] * S[m - 1, -1])
    return 1.05 * (th[-1] + resid)


def chebyshev_exp(applyA, v, dt, lam_max, nterms):
    """exp(-dt A) v via a Chebyshev expansion on [0, lam_max] (A symmetric psd).

    With s = (2 A - L I)/L (spectrum in [-1,1]) and a = dt L / 2:
        exp(-dt A) = e^{-a} exp(-a s) = sum_k c_k T_k(s),   c_k = 2 (-1)^k e^{-a} I_k(a)
    (I_k = modified Bessel function; scipy.special.ive(k,a) = e^{-a} I_k(a)).
    Costs nterms applications of A, three vectors of storage, no inner products.
    The degree needed grows like dt*lam_max (compare with sqrt(dt*lam_max) for Lanczos).
    """
    L = float(lam_max)
    a = dt * L / 2.0
    k = np.arange(nterms)
    ck = 2.0 * (-1.0) ** k * spec.ive(k, a)
    ck[0] /= 2.0
    Tprev = v.CreateVector(); Tcur = v.CreateVector(); Tnext = v.CreateVector()
    Tprev.data = v
    Av = applyA(Tprev)
    Tcur.data = (2.0 / L) * Av - Tprev
    res = v.CreateVector()
    res.data = float(ck[0]) * Tprev + float(ck[1]) * Tcur
    for kk in range(2, nterms):
        Av = applyA(Tcur)
        Tnext.data = (4.0 / L) * Av - 2.0 * Tcur - Tprev
        res.data += float(ck[kk]) * Tnext
        Tprev.data = Tcur
        Tcur.data = Tnext
    return res


# ----------------------------------------------------------------------------------
# rational alternative: contour integral (Cauchy formula on a parabolic contour)
# ----------------------------------------------------------------------------------

class ContourExp(BaseMatrix):
    """f(-dt A) x by the Cauchy integral on a parabolic contour (Weideman & Trefethen 2007).

        f(-dt A) v = 1/(2 pi i) \\oint f(dt z) (z I + A)^{-1} v dz
                   = 1/(2 pi i) \\oint f(dt z) (z M + K)^{-1} M v dz

    Contour:  z(theta) = (N/dt) (0.1309 - 0.1194 theta^2 + 0.25 i theta), theta in (-pi, pi),
    midpoint rule with N points; error O(2.85^{-N}).  By conjugate symmetry only the N/2
    points with theta > 0 are needed for real data.  The N/2 complex factorisations of
    z_k M + K are computed once in the constructor (M, K must be assembled on a complex
    FESpace); each apply costs N/2 complex back-substitutions and no inner products.
    All phi-functions share the same poles: pass func=lambda z: phi(1, z) etc.
    """

    def __init__(self, Mc, Kc, dt, freedofs, N=24, inverse="umfpack", M=None):
        """M: optional real mass matrix; if given, vectors created by this operator are real
        (so that `(C * v).Evaluate()` is a real vector for real v)."""
        super().__init__()
        self.Mc, self.Kc, self.dt, self.N = Mc, Kc, dt, N
        self.Mreal = M
        self.P = Projector(freedofs, True)
        self._freedofs = freedofs
        th = (np.arange(N // 2) + 0.5) * 2 * np.pi / N            # theta > 0 half
        self.z = (N / dt) * (0.1309 - 0.1194 * th ** 2 + 0.25j * th)
        self.dz = (N / dt) * (-2 * 0.1194 * th + 0.25j)
        self.invs = []
        Z = Mc.CreateMatrix()
        for zk in self.z:
            Z.AsVector().data = complex(zk) * Mc.AsVector() + Kc.AsVector()
            self.invs.append(Z.Inverse(freedofs, inverse=inverse))
        self.rhs = Kc.CreateColVector()
        self.acc = Kc.CreateColVector()

    def Height(self): return self.Mc.height
    def Width(self): return self.Mc.width
    def IsComplex(self): return self.Mreal is None
    def CreateRowVector(self): return (self.Mreal or self.Mc).CreateRowVector()
    def CreateColVector(self): return (self.Mreal or self.Mc).CreateColVector()

    def Apply(self, x, func=np.exp):
        """func(-dt A) x for a real or complex BaseVector x; returns a vector like x."""
        xc = self.Kc.CreateColVector()
        xc.FV().NumPy()[:] = x.FV().NumPy()
        xc.data = self.P * xc
        self.rhs.data = self.Mc * xc
        self.acc[:] = 0.0
        w = func(self.dt * self.z) * self.dz / (1j * self.N)   # (2 pi/N) / (2 pi i) * f * dz
        for wk, inv in zip(w, self.invs):
            self.acc.data += complex(wk) * (inv * self.rhs)
        out = x.CreateVector()
        out.FV().NumPy()[:] = 2 * self.acc.FV().NumPy().real   # conjugate symmetry
        return out

    def Mult(self, x, y):
        y.data = self.Apply(x, np.exp)

    def Phi(self, k, x):
        """phi_k(-dt A) x.

        phi_k(dt z) decays only like 1/z along the contour, so the truncated trapezoid
        rule would converge algebraically.  We therefore use the recursion
            phi_k(-dt A) = -(dt A)^{-1} (phi_{k-1}(-dt A) - I/(k-1)!),   phi_0 = exp,
        which needs one factorisation of K (done lazily, once) and reuses the exp contour.
        (Cancellation of about log10(1/(dt lambda_min)) digits for the smooth modes.)
        """
        if k == 0:
            return self.Apply(x, np.exp)
        if not hasattr(self, "invK"):
            self.invK = self.Kc.Inverse(self._freedofs, inverse="umfpack")
        prev = self.Phi(k - 1, x)                       # phi_{k-1}(-dt A) x
        r = prev.CreateVector()
        r.data = prev - (1.0 / factorial(k - 1)) * x
        r.data = self.P * r
        # -(dt A)^{-1} r = -(1/dt) K^{-1} M r
        rc = self.Kc.CreateColVector(); rc.FV().NumPy()[:] = r.FV().NumPy()
        mr = self.Kc.CreateColVector(); mr.data = self.Mc * rc
        sol = self.Kc.CreateColVector(); sol.data = self.invK * mr
        out = x.CreateVector()
        out.FV().NumPy()[:] = (-1.0 / self.dt) * (sol.FV().NumPy() if out.is_complex else sol.FV().NumPy().real)
        return out


# ----------------------------------------------------------------------------------
# dense reference solution on coarse meshes (for tests and convergence plots)
# ----------------------------------------------------------------------------------

class DenseReference:
    """Exact f(A) v on the free dofs via the dense generalised eigenproblem K W = M W Lambda.

    Requires the forms to be assembled with symmetric=False (so that COO() is complete).
    W is M-orthonormal, hence  f(A) v = W f(Lambda) W^T M v.
    """

    def __init__(self, K, M, freedofs):
        self.idx = np.array([i for i in range(M.height) if freedofs[i]])
        self.Kd = self._dense(K)
        self.Md = self._dense(M)
        self.lam, self.W = sla.eigh(self.Kd, self.Md)

    def _dense(self, mat):
        r, c, val = mat.COO()
        D = sp.csr_matrix((val, (r, c)), shape=(mat.height, mat.width)).toarray()
        return D[np.ix_(self.idx, self.idx)]

    def to_np(self, vec):
        return np.array(vec.FV().NumPy())[self.idx]

    def apply(self, func, vnp):
        """func(A) v for a numpy vector v on the free dofs."""
        return self.W @ (func(self.lam) * (self.W.T @ (self.Md @ vnp)))

    def norm(self, vnp):
        return sqrt(abs(np.conj(vnp) @ (self.Md @ vnp)))

    def relerr(self, vec, ref_np):
        """relative M-norm error of the BaseVector vec against a numpy reference."""
        v = self.to_np(vec) if isinstance(vec, BaseVector) else np.asarray(vec)[self.idx] if len(vec) != len(self.idx) else np.asarray(vec)
        return self.norm(v - ref_np) / self.norm(ref_np)
