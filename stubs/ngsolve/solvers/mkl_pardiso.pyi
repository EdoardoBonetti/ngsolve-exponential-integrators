from __future__ import annotations
from contextlib import contextmanager
import ctypes as ctypes
from netgen import TimeFunction
from ngsolve import config
from ngsolve import la as ngla
import ngsolve.la
import numpy as np
from pyngcore.pyngcore import SuspendTaskManager
from pyngcore.pyngcore.pybind11_detail_function_record_v1_system_libcpp_abi1 import GetNumThreads
import typing
__all__ = ['GetNumThreads', 'MKLPardiso', 'MKLPardisoSPD', 'SuspendTaskManager', 'TimeFunction', 'config', 'contextmanager', 'ctypes', 'ngla', 'np']
class MKLPardiso(ngsolve.la.SparseFactorizationInterface):
    _orderings: typing.ClassVar[dict] = {'minimum_degree': 0, 'metis': 2, 'parallel_metis': 3}
    is_spd: typing.ClassVar[bool] = False
    @staticmethod
    def Analyze(*args, **kwargs):
        ...
    @staticmethod
    def Factor(*args, **kwargs):
        ...
    @staticmethod
    def Solve(*args, **kwargs):
        ...
    @staticmethod
    def SolveConjTrans(*args, **kwargs):
        ...
    @staticmethod
    def SolveTrans(*args, **kwargs):
        ...
    @staticmethod
    def _as_ctypes(arr):
        ...
    def __del__(self):
        ...
    def __init__(self, *args, msglevel = 0, params: dict[int, int] | None = None, **kwargs):
        ...
    def _apply_flags(self, flags):
        """
        ordering: minimum_degree|metis|parallel_metis, refinement: max iterative refinement
        steps, symmetric: use the symmetric matrix type (caller asserts A == A^T),
        msglevel, iparmN: raw MKL iparm[N]
        """
    def _call_pardiso(self, phase):
        ...
    def _release(self):
        ...
    def _solve_flag(self, b, sol, flag):
        ...
    def get_csr(self):
        ...
class MKLPardisoSPD(MKLPardiso):
    is_spd: typing.ClassVar[bool] = True
def _find_mkl():
    ...
def _mkl_threads(*args, **kwds):
    ...
_mkl_free_buffers = None
_mkl_set_num_threads_local = None
_pardiso = None
