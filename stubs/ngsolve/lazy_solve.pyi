from __future__ import annotations
import atexit as atexit
import netgen as netgen
from netgen import Redraw
from netgen import TimeFunction
import ngsolve as ngslib
from ngsolve import bla
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import InnerProduct
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Matrix
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Norm
from ngsolve.bla.pybind11_detail_function_record_v1_system_libcpp_abi1 import Vector
from ngsolve import bvp
import ngsolve.comp
from ngsolve import comp
from ngsolve.comp import APhiHCurlAMG
from ngsolve.comp import BilinearForm
from ngsolve.comp import COUPLING_TYPE
from ngsolve.comp import Compress
from ngsolve.comp import ContactBoundary
from ngsolve.comp import ContactIntegrator
from ngsolve.comp import DirichletBC
from ngsolve.comp import Discontinuous
from ngsolve.comp import ElementId
from ngsolve.comp import FESpace
from ngsolve.comp import FacetFESpace
from ngsolve.comp import FacetSurface
from ngsolve.comp import GridFunction
from ngsolve.comp import H1
from ngsolve.comp import H1LumpingFESpace
from ngsolve.comp import HCT_FESpace
from ngsolve.comp import HCurl
from ngsolve.comp import HCurlAMG
from ngsolve.comp import HCurlCurl
from ngsolve.comp import HCurlDiv
from ngsolve.comp import HDiv
from ngsolve.comp import HDivDiv
from ngsolve.comp import HDivDivFacetSpace
from ngsolve.comp import HDivDivSurface
from ngsolve.comp import HDivSurface
from ngsolve.comp import Hidden as PrivateSpace
from ngsolve.comp import Hidden
from ngsolve.comp import JKM_FESpace
from ngsolve.comp import L2
from ngsolve.comp import LinearForm
from ngsolve.comp import MatrixValued
from ngsolve.comp import Mesh
from ngsolve.comp import MultiGridPreconditioner
from ngsolve.comp import NodalFESpace
from ngsolve.comp import NodeId
from ngsolve.comp import NormalFacetFESpace
from ngsolve.comp import NormalFacetSurface
from ngsolve.comp import NumberSpace
from ngsolve.comp import ORDER_POLICY
from ngsolve.comp import Periodic
from ngsolve.comp import PlateauFESpace
from ngsolve.comp import Preconditioner
from ngsolve.comp import PreconditionerCreator
from ngsolve.comp import ProductSpace
from ngsolve.comp import Region
from ngsolve.comp import SurfaceL2
from ngsolve.comp import TangentialFacetFESpace
from ngsolve.comp import TangentialSurfaceL2
from ngsolve.comp import VTKOutput
from ngsolve.comp import Variation
from ngsolve.comp import VariationalEquation
from ngsolve.comp import VectorFacetFESpace
from ngsolve.comp import VectorFacetSurface
from ngsolve.comp import VectorH1
from ngsolve.comp import VectorL2
from ngsolve.comp import VectorNodalFESpace
from ngsolve.comp import VectorSurfaceL2
from ngsolve.comp import VectorValued
from ngsolve.comp import pml
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import BoundaryFromVolumeCF
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompressCompound
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import ConvertOperator
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import Integrate
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import Interpolate
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import PatchwiseSolve
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetHeapSize
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetTestoutFile
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicBFI
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicEnergy
from ngsolve.comp.pybind11_detail_function_record_v1_system_libcpp_abi1 import SymbolicLFI
from ngsolve import config
from ngsolve import directsolvers
from ngsolve import eigenvalues
import ngsolve.fem
from ngsolve import fem
from ngsolve.fem import BFI
from ngsolve.fem import BSpline
from ngsolve.fem import CoefficientFunction
from ngsolve.fem import ET
from ngsolve.fem import IntegrationRule
from ngsolve.fem import LFI
from ngsolve.fem import Parameter
from ngsolve.fem import ParameterC
from ngsolve.fem import PlaceholderCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import BlockBFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import BlockLFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CacheCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Cof
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompoundBFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import CompoundLFI
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Conj
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Cross
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Det
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Id
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import IfPos
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Inv
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Skew
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Sym
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Trace
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import VoxelCoefficient
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import Zero as ZeroCF
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import acos
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import acosh
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import asin
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import asinh
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import atan
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import atan2
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import ceil
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import cos
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import cosh
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import erf
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import exp
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import floor
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import log
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import pow
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import sin
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import sinh
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import sqrt
from ngsolve.fem.pybind11_detail_function_record_v1_system_libcpp_abi1 import tan
from ngsolve import krylovspace
from ngsolve.krylovspace import CGSolver
from ngsolve.krylovspace import DeviceCGSolver
from ngsolve.krylovspace import DeviceTFQMRSolver
from ngsolve.krylovspace import GMRESSolver
from ngsolve.krylovspace import LinearSolverCreator
from ngsolve.krylovspace import QMRSolver
from ngsolve import la
from ngsolve.la import BaseMatrix
from ngsolve.la import BaseVector
from ngsolve.la import BlockMatrix
from ngsolve.la import BlockVector
from ngsolve.la import ConstEBEMatrix
from ngsolve.la import DiagonalMatrix
from ngsolve.la import Embedding
from ngsolve.la import IdentityMatrix
from ngsolve.la import MultiVector
from ngsolve.la import PARALLEL_STATUS
from ngsolve.la import PermutationMatrix
from ngsolve.la import Projector
from ngsolve.la import SparseFactorizationCreator
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import ArnoldiSolver
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import CreateVVector
from ngsolve.la.pybind11_detail_function_record_v1_system_libcpp_abi1 import ParallelMatrix
from ngsolve import ngstd
from ngsolve.ngstd import IntRange
from ngsolve import nonlinearsolvers
from ngsolve import preconditioners
from ngsolve import solve
from ngsolve.solve.pybind11_detail_function_record_v1_system_libcpp_abi1 import Draw
from ngsolve.solve.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetVisualization
from ngsolve import solvers
from ngsolve import timestepping
from ngsolve import utils
from ngsolve.utils import Deviator
from ngsolve.utils import Grad
from ngsolve.utils import Normalize
from ngsolve.utils import OuterProduct
from ngsolve.utils import PyCof
from ngsolve.utils import PyCross
from ngsolve.utils import PyDet
from ngsolve.utils import PyId
from ngsolve.utils import PyInv
from ngsolve.utils import PySkew
from ngsolve.utils import PySym
from ngsolve.utils import PyTrace
from ngsolve.utils import curl
from ngsolve.utils import div
from ngsolve.utils import grad
from ngsolve.utils import printonce
import os as os
from pyngcore.pyngcore import BitArray
from pyngcore.pyngcore import PajeTrace
from pyngcore.pyngcore import TaskManager
from pyngcore.pyngcore import Timer
from pyngcore.pyngcore.pybind11_detail_function_record_v1_system_libcpp_abi1 import GetNumThreads
from pyngcore.pyngcore.pybind11_detail_function_record_v1_system_libcpp_abi1 import SetNumThreads
from pyngcore.pyngcore.pybind11_detail_function_record_v1_system_libcpp_abi1 import Timers
import sys as sys
__all__ = ['APhiHCurlAMG', 'ArnoldiSolver', 'BBBND', 'BBND', 'BFI', 'BND', 'BSpline', 'BaseMatrix', 'BaseVector', 'BilinearForm', 'BitArray', 'BlockBFI', 'BlockLFI', 'BlockMatrix', 'BlockVector', 'BoundaryFromVolumeCF', 'CELL', 'CGSolver', 'COUPLING_TYPE', 'CacheCF', 'CoefficientFunction', 'Cof', 'CompoundBFI', 'CompoundLFI', 'Compress', 'CompressCompound', 'Conj', 'ConstEBEMatrix', 'ContactBoundary', 'ContactIntegrator', 'ConvertOperator', 'CreateVVector', 'Cross', 'Det', 'Deviator', 'DeviceCGSolver', 'DeviceTFQMRSolver', 'DiagonalMatrix', 'DirichletBC', 'Discontinuous', 'Draw', 'EDGE', 'ELEMENT', 'ET', 'ElementId', 'Embedding', 'FACE', 'FACET', 'FESpace', 'FacetFESpace', 'FacetSurface', 'GMRESSolver', 'GetNumThreads', 'Grad', 'GridFunction', 'H1', 'H1LumpingFESpace', 'HCT_FESpace', 'HCurl', 'HCurlAMG', 'HCurlCurl', 'HCurlDiv', 'HDiv', 'HDivDiv', 'HDivDivFacetSpace', 'HDivDivSurface', 'HDivSurface', 'HEX', 'Hidden', 'Id', 'IdentityMatrix', 'IfPos', 'InnerProduct', 'IntRange', 'Integrate', 'IntegrationRule', 'Interpolate', 'Inv', 'JKM_FESpace', 'L2', 'LFI', 'LinearForm', 'LinearSolverCreator', 'Matrix', 'MatrixValued', 'Mesh', 'MultiGridPreconditioner', 'MultiVector', 'NodalFESpace', 'NodeId', 'Norm', 'NormalFacetFESpace', 'NormalFacetSurface', 'Normalize', 'NumberSpace', 'ORDER_POLICY', 'OuterProduct', 'PARALLEL_STATUS', 'POINT', 'PRISM', 'PYRAMID', 'PajeTrace', 'ParallelMatrix', 'Parameter', 'ParameterC', 'PatchwiseSolve', 'Periodic', 'PermutationMatrix', 'PlaceholderCF', 'PlateauFESpace', 'Preconditioner', 'PreconditionerCreator', 'PrivateSpace', 'ProductSpace', 'Projector', 'PyCof', 'PyCross', 'PyDet', 'PyId', 'PyInv', 'PySkew', 'PySym', 'PyTrace', 'QMRSolver', 'QUAD', 'Redraw', 'Region', 'SEGM', 'SetHeapSize', 'SetNumThreads', 'SetTestoutFile', 'SetVisualization', 'Skew', 'SolveVE', 'SparseFactorizationCreator', 'SurfaceL2', 'Sym', 'SymbolicBFI', 'SymbolicEnergy', 'SymbolicLFI', 'TET', 'TRIG', 'TangentialFacetFESpace', 'TangentialSurfaceL2', 'TaskManager', 'TimeFunction', 'Timer', 'Timers', 'Trace', 'VERTEX', 'VOL', 'VTKOutput', 'Variation', 'VariationalEquation', 'VariationalEquationSolver', 'Vector', 'VectorFacetFESpace', 'VectorFacetSurface', 'VectorH1', 'VectorL2', 'VectorNodalFESpace', 'VectorSurfaceL2', 'VectorValued', 'VoxelCoefficient', 'ZeroCF', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atexit', 'bla', 'bvp', 'ceil', 'comp', 'config', 'cos', 'cosh', 'curl', 'directsolvers', 'div', 'dl', 'ds', 'dx', 'eigenvalues', 'erf', 'exp', 'fem', 'floor', 'grad', 'krylovspace', 'la', 'log', 'netgen', 'ngsglobals', 'ngslib', 'ngstd', 'nonlinearsolvers', 'os', 'pml', 'pow', 'preconditioners', 'printonce', 'sin', 'sinh', 'solve', 'solvers', 'specialcf', 'sqrt', 'sys', 'tan', 'timestepping', 'utils', 'x', 'y', 'z']
class VariationalEquationSolver:
    def Solve(self):
        ...
    def __init__(self, equation, *args: ngsolve.comp.DirichletBC | ngsolve.comp.Preconditioner, verbose = 0, **kwargs):
        ...
def SolveVE(equation, *args, **kwargs):
    ...
BBBND: ngsolve.comp.VorB  # value = <VorB.BBBND: 3>
BBND: ngsolve.comp.VorB  # value = <VorB.BBND: 2>
BND: ngsolve.comp.VorB  # value = <VorB.BND: 1>
CELL: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.CELL: 3>
EDGE: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.EDGE: 1>
ELEMENT: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.ELEMENT: 4>
FACE: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.FACE: 2>
FACET: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.FACET: 5>
HEX: ngsolve.fem.ET  # value = <ET.HEX: 24>
POINT: ngsolve.fem.ET  # value = <ET.POINT: 0>
PRISM: ngsolve.fem.ET  # value = <ET.PRISM: 22>
PYRAMID: ngsolve.fem.ET  # value = <ET.PYRAMID: 21>
QUAD: ngsolve.fem.ET  # value = <ET.QUAD: 11>
SEGM: ngsolve.fem.ET  # value = <ET.SEGM: 1>
TET: ngsolve.fem.ET  # value = <ET.TET: 20>
TRIG: ngsolve.fem.ET  # value = <ET.TRIG: 10>
VERTEX: ngsolve.fem.NODE_TYPE  # value = <NODE_TYPE.VERTEX: 0>
VOL: ngsolve.comp.VorB  # value = <VorB.VOL: 0>
dl: ngsolve.comp.DifferentialSymbol  # value = <ngsolve.comp.DifferentialSymbol object>
ds: ngsolve.comp.DifferentialSymbol  # value = <ngsolve.comp.DifferentialSymbol object>
dx: ngsolve.comp.DifferentialSymbol  # value = <ngsolve.comp.DifferentialSymbol object>
ngsglobals: ngsolve.comp.GlobalVariables  # value = <ngsolve.comp.GlobalVariables object>
specialcf: ngsolve.fem.SpecialCFCreator  # value = <ngsolve.fem.SpecialCFCreator object>
x: ngsolve.fem.CoefficientFunction  # value = <ngsolve.fem.CoefficientFunction object>
y: ngsolve.fem.CoefficientFunction  # value = <ngsolve.fem.CoefficientFunction object>
z: ngsolve.fem.CoefficientFunction  # value = <ngsolve.fem.CoefficientFunction object>
