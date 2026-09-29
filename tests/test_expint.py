"""
pytest suite for expint_tools (run from the repository root):

    PYTHONPATH=/Applications/Netgen.app/Contents/Resources/lib/python3.13/site-packages \
      /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m pytest tests -q

All tests use small meshes so that a dense generalised eigendecomposition can serve as
the exact reference.  Thresholds are ~10x the errors measured while developing the tools.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import scipy.linalg as sla
import pytest
from ngsolve import *
from expint_tools import (phi, krylov_funm, KrylovExp, ContourExp, chebyshev_exp,
                          lanczos_spectral_bound, DenseReference)

ngsglobals.msg_level = 0


# ----------------------------------------------------------------------------- fixtures
@pytest.fixture(scope="module")
def heat():
    mesh = Mesh(unit_square.GenerateMesh(maxh=0.12))
    fes = H1(mesh, order=3, dirichlet=".*")
    u, v = fes.TnT()
    K = BilinearForm(grad(u) * grad(v) * dx, symmetric=False).Assemble().mat
    M = BilinearForm(u * v * dx, symmetric=False).Assemble().mat
    fd = fes.FreeDofs()
    P = Projector(fd, True)
    gfu = GridFunction(fes)
    gfu.Set(exp(-200 * ((x - 0.5) ** 2 + (y - 0.5) ** 2)) + IfPos(x - 0.7, 1, 0) * IfPos(y - 0.7, 1, 0))
    gfu.vec.data = P * gfu.vec                       # rough datum on the free dofs
    ref = DenseReference(K, M, fd)
    fesc = H1(mesh, order=3, dirichlet=".*", complex=True)
    uc, vc = fesc.TnT()
    Kc = BilinearForm(grad(uc) * grad(vc) * dx, symmetric=False).Assemble().mat
    Mc = BilinearForm(uc * vc * dx, symmetric=False).Assemble().mat
    lf = LinearForm(fes); lf += 1 * v * dx; lf.Assemble()
    return dict(mesh=mesh, fes=fes, K=K, M=M, fd=fd, P=P, u0=gfu.vec, ref=ref,
                fesc=fesc, Kc=Kc, Mc=Mc, f=lf.vec)


# ----------------------------------------------------------------------------- scalar phi
def test_phi_scalar():
    z = np.array([-1e-9, -0.1, -0.49, -0.51, -3.0, -50.0, 0.3, 2.0])
    assert np.allclose(phi(0, z), np.exp(z))
    ref1 = np.where(z == 0, 1.0, np.expm1(z) / np.where(z == 0, 1, z))
    assert np.allclose(phi(1, z), ref1, rtol=1e-13, atol=1e-15)
    zz = np.array([-0.3, -4.0, 1.5])
    assert np.allclose(phi(2, zz), (np.exp(zz) - 1 - zz) / zz ** 2, rtol=1e-12)
    assert phi(1, np.array([-np.inf]))[0] == 0.0
    assert abs(phi(1, np.array([0.0]))[0] - 1.0) < 1e-15
    zc = np.array([-0.2 + 0.1j, 3 + 2j])
    assert np.allclose(phi(1, zc), (np.exp(zc) - 1) / zc)


# ----------------------------------------------------------------------------- exp(-dt A) v
def test_eigenmode_decay(heat):
    """u0 = sin(pi x) sin(pi y) decays like exp(-2 pi^2 t); checks the whole pipeline."""
    fes, M, K, fd = heat["fes"], heat["M"], heat["K"], heat["fd"]
    gfu = GridFunction(fes); gfu.Set(sin(pi * x) * sin(pi * y)); gfu.vec.data = heat["P"] * gfu.vec
    dt, nsteps = 0.01, 10
    E = KrylovExp(M, K, dt, fd, tol=1e-10)
    for _ in range(nsteps):
        gfu.vec.data = E * gfu.vec
    exact = np.exp(-2 * pi ** 2 * dt * nsteps) * sin(pi * x) * sin(pi * y)
    err = sqrt(Integrate((gfu - exact) ** 2, heat["mesh"]))
    assert err < 1e-5                                  # p=3 discretisation error floor
    assert E.info["m"] <= 6                            # a single mode converges immediately


def test_poly_lanczos_vs_dense(heat):
    M, K, fd, ref, u0 = heat["M"], heat["K"], heat["fd"], heat["ref"], heat["u0"]
    dt = 0.01
    ex = ref.apply(lambda l: np.exp(-dt * l), ref.to_np(u0))
    E = KrylovExp(M, K, dt, fd, poly=True, tol=0.0, maxm=120)
    errs = []
    for m in [20, 40, 80, 120]:
        E.maxm = m
        errs.append(ref.relerr((E * u0).Evaluate(), ex))
    assert errs[-1] < 1e-8
    assert all(np.diff(np.log(errs)) < 0)              # monotone convergence


def test_si_lanczos_vs_dense(heat):
    M, K, fd, ref, u0 = heat["M"], heat["K"], heat["fd"], heat["ref"], heat["u0"]
    for dt in [1e-3, 1e-2, 1e-1]:
        ex = ref.apply(lambda l: np.exp(-dt * l), ref.to_np(u0))
        E = KrylovExp(M, K, dt, fd, tol=0.0, maxm=24)
        assert ref.relerr((E * u0).Evaluate(), ex) < 1e-8, dt
        E = KrylovExp(M, K, dt, fd, tol=1e-10)         # adaptive
        assert ref.relerr((E * u0).Evaluate(), ex) < 1e-8
        assert E.info["m"] <= 40


def test_chebyshev_vs_dense(heat):
    M, K, fd, ref, u0 = heat["M"], heat["K"], heat["fd"], heat["ref"], heat["u0"]
    dt = 0.01
    ex = ref.apply(lambda l: np.exp(-dt * l), ref.to_np(u0))
    invM = M.Inverse(fd, inverse="sparsecholesky")
    tmp = M.CreateColVector()
    def applyA(xv):
        out = M.CreateColVector(); tmp.data = K * xv; out.data = invM * tmp; return out
    L = lanczos_spectral_bound(applyA, M, u0, 30)
    assert ref.lam[-1] <= L <= 1.2 * ref.lam[-1]
    n = int(dt * L / 2) + 40                           # degree ~ dt*lam_max/2 + margin
    assert ref.relerr(chebyshev_exp(applyA, u0, dt, L, n), ex) < 1e-8


def test_contour_vs_dense(heat):
    Mc, Kc, fesc, ref, u0 = heat["Mc"], heat["Kc"], heat["fesc"], heat["ref"], heat["u0"]
    dt = 0.01
    ex = ref.apply(lambda l: np.exp(-dt * l), ref.to_np(u0))
    errs = [ref.relerr((ContourExp(Mc, Kc, dt, fesc.FreeDofs(), N=N) * u0).Evaluate(), ex)
            for N in [8, 16, 24]]
    assert errs[2] < 1e-9 and errs[1] < 1e-6 and errs[0] < 1e-2


# ----------------------------------------------------------------------------- phi-functions
def test_phi1_constant_source(heat):
    M, K, fd, ref, f = heat["M"], heat["K"], heat["fd"], heat["ref"], heat["f"]
    dt = 0.01
    invM = M.Inverse(fd, inverse="sparsecholesky")
    g = M.CreateColVector(); g.data = invM * f
    gnp = ref.to_np(g)
    E = KrylovExp(M, K, dt, fd, tol=1e-10)
    for k in [1, 2]:
        ex = ref.apply(lambda l: phi(k, -dt * l), gnp)
        assert ref.relerr(E.Phi(k, g), ex) < 1e-8
    C = ContourExp(heat["Mc"], heat["Kc"], dt, heat["fesc"].FreeDofs(), N=24)
    ex1 = ref.apply(lambda l: phi(1, -dt * l), gnp)
    assert ref.relerr(C.Phi(1, g), ex1) < 1e-8
    # exponential Euler with constant source reaches the steady state K u = f
    gfu = GridFunction(heat["fes"]); gfu.vec[:] = 0.0
    step_g = E.Phi(1, g)                               # dt*phi1(-dt A) M^{-1} f  (dt factor below)
    for _ in range(100):
        gfu.vec.data = E * gfu.vec + dt * step_g
    steady = K.Inverse(fd, inverse="sparsecholesky") * f
    d = gfu.vec.CreateVector(); d.data = gfu.vec - steady
    assert sqrt(InnerProduct(d, M * d)) / sqrt(InnerProduct(steady, M * steady)) < 1e-6


def test_zero_start_vector(heat):
    M, K, fd = heat["M"], heat["K"], heat["fd"]
    E = KrylovExp(M, K, 0.01, fd)
    z = M.CreateColVector(); z[:] = 0.0
    assert Norm((E * z).Evaluate()) == 0.0 and E.info["m"] == 0


# ----------------------------------------------------------------------------- time stepping
def test_orders_IE_CN_expEuler(heat):
    """implicit Euler order 1, Crank-Nicolson order 2, exponential Euler exact in time."""
    fes, M, K, fd, ref = heat["fes"], heat["M"], heat["K"], heat["fd"], heat["ref"]
    u, v = fes.TnT()
    lf = LinearForm(fes); lf += sin(pi * x) * sin(pi * y) * v * dx; lf.Assemble()
    gfu = GridFunction(fes); gfu.Set(sin(pi * x) * sin(pi * y)); gfu.vec.data = heat["P"] * gfu.vec
    u0np = ref.to_np(gfu.vec); fnp = ref.to_np(lf.vec)
    Tend = 0.2
    exact = ref.apply(lambda l: np.exp(-Tend * l), u0np) + \
        ref.W @ ((1 - np.exp(-Tend * ref.lam)) / ref.lam * (ref.W.T @ fnp))
    invM = M.Inverse(fd, inverse="sparsecholesky")

    def theta_scheme(theta, dt):
        mstar = M.CreateMatrix(); mstar.AsVector().data = M.AsVector() + theta * dt * K.AsVector()
        inv = mstar.Inverse(fd, inverse="sparsecholesky")
        w = gfu.vec.CreateVector(); w.data = gfu.vec
        for _ in range(int(round(Tend / dt))):
            w.data = inv * (M * w - (1 - theta) * dt * (K * w) + dt * lf.vec)
        return ref.relerr(w, exact)

    def exp_euler(dt):
        E = KrylovExp(M, K, dt, fd, tol=1e-10)
        g = E.Phi(1, invM * lf.vec)
        w = gfu.vec.CreateVector(); w.data = gfu.vec
        for _ in range(int(round(Tend / dt))):
            w.data = E * w + dt * g
        return ref.relerr(w, exact)

    dts = [0.04, 0.02, 0.01, 0.005]
    eIE = [theta_scheme(1.0, dt) for dt in dts]
    eCN = [theta_scheme(0.5, dt) for dt in dts]
    eEE = [exp_euler(dt) for dt in dts]
    oIE = np.log2(eIE[-2] / eIE[-1]); oCN = np.log2(eCN[-2] / eCN[-1])
    assert 0.8 < oIE < 1.2, eIE
    assert 1.8 < oCN < 2.2, eCN
    assert max(eEE) < 1e-7, eEE


# ----------------------------------------------------------------------------- non-symmetric
def test_convdiff_arnoldi_vs_expm(heat):
    fes, M, fd, ref, u0 = heat["fes"], heat["M"], heat["fd"], heat["ref"], heat["u0"]
    u, v = fes.TnT()
    b = CoefficientFunction((2 * y * (1 - x * x), -2 * x * (1 - y * y)))
    Kcd = BilinearForm(0.01 * grad(u) * grad(v) * dx + b * grad(u) * v * dx, symmetric=False).Assemble().mat
    dt = 0.01
    Acd = np.linalg.solve(ref.Md, ref._dense(Kcd))
    ex = sla.expm(-dt * Acd) @ ref.to_np(u0)
    E = KrylovExp(M, Kcd, dt, fd, tol=1e-11, symmetric=False)
    res = (E * u0).Evaluate()
    assert ref.norm(ref.to_np(res) - ex) / ref.norm(ex) < 1e-9
    assert E.info["m"] <= 30


# ----------------------------------------------------------------------------- nonlinear
def test_allen_cahn_orders():
    """exponential Euler (order 1) and exponential Rosenbrock-Euler (order 2) for
    u_t = eps Laplace u + u - u^3 with Neumann boundary conditions."""
    mesh = Mesh(unit_square.GenerateMesh(maxh=0.2))
    fes = H1(mesh, order=2)
    u, v = fes.TnT()
    eps = 0.05
    K = BilinearForm(eps * grad(u) * grad(v) * dx, symmetric=False).Assemble().mat
    M = BilinearForm(u * v * dx, symmetric=False).Assemble().mat
    fd = fes.FreeDofs()
    invM = M.Inverse(fd, inverse="sparsecholesky")
    gfu = GridFunction(fes)
    u0 = 0.5 * cos(2 * pi * x) * cos(pi * y)
    lf = LinearForm(fes); lf += (gfu - gfu ** 3) * v * dx
    Tend = 0.4

    def exp_euler(dt):
        gfu.Set(u0)
        E = KrylovExp(M, K, dt, fd, tol=1e-10)
        for _ in range(int(round(Tend / dt))):
            lf.Assemble()
            g = E.Phi(1, invM * lf.vec)
            gfu.vec.data = E * gfu.vec + dt * g
        return gfu.vec.FV().NumPy().copy()

    def exp_rosenbrock_euler(dt):
        gfu.Set(u0)
        for _ in range(int(round(Tend / dt))):
            lf.Assemble()
            jac = BilinearForm(eps * grad(u) * grad(v) * dx - (1 - 3 * gfu ** 2) * u * v * dx,
                               symmetric=False).Assemble().mat
            F = M.CreateColVector(); F.data = lf.vec - K * gfu.vec          # M u' = F(u)
            E = KrylovExp(M, jac, dt, fd, tol=1e-10, inverse="umfpack")   # phi1(-dt M^{-1} J)
            gfu.vec.data += dt * E.Phi(1, invM * F)
        return gfu.vec.FV().NumPy().copy()

    refsol = exp_rosenbrock_euler(0.0025)
    nrm = lambda w: sqrt(w @ (M.ToDense().NumPy() @ w)) if False else np.linalg.norm(w)
    dts = [0.1, 0.05, 0.025]
    eEE = [nrm(exp_euler(dt) - refsol) for dt in dts]
    eRB = [nrm(exp_rosenbrock_euler(dt) - refsol) for dt in dts]
    oEE = np.log2(eEE[-2] / eEE[-1]); oRB = np.log2(eRB[-2] / eRB[-1])
    assert 0.8 < oEE < 1.3, (eEE, oEE)
    assert 1.7 < oRB < 2.4, (eRB, oRB)
