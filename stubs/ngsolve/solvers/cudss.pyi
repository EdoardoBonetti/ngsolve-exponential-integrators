from __future__ import annotations
from importlib import metadata as importlib_metadata
from importlib import util as importlib_util
from netgen import TimeFunction
from ngsolve import la as ngla
import ngsolve.la
import numpy as np
import numpy
import os as os
import pathlib as pathlib
import typing
__all__ = ['CudssSolver', 'CudssSolverFloat32', 'CudssSolverFloat32SPD', 'CudssSolverSPD', 'TimeFunction', 'importlib_metadata', 'importlib_util', 'make_directsolver_options', 'ngla', 'np', 'os', 'pathlib']
class CudssSolver(ngsolve.la.SparseFactorizationInterface):
    solver = None
    spd: typing.ClassVar[bool] = False
    dtype = numpy.float64
    @staticmethod
    def Analyze(*args, **kwargs):
        ...
    @staticmethod
    def Factor(*args, **kwargs):
        ...
    @staticmethod
    def Solve(*args, **kwargs):
        ...
    def __del__(self):
        ...
class CudssSolverFloat32(CudssSolver):
    dtype = numpy.float32
class CudssSolverFloat32SPD(CudssSolver):
    spd: typing.ClassVar[bool] = True
    dtype = numpy.float32
class CudssSolverSPD(CudssSolver):
    spd: typing.ClassVar[bool] = True
def _from_dist_files():
    ...
def _stream_package(solver):
    ...
def make_directsolver_options():
    ...
