"""
pybind la
"""
from __future__ import annotations
import collections.abc
import ngsolve.bla
from ngsolve.krylovspace import CGSolver
from ngsolve.krylovspace import DeviceCGSolver
from ngsolve.krylovspace import DeviceTFQMRSolver
from ngsolve.krylovspace import GMRESSolver
from ngsolve.krylovspace import QMRSolver
import ngsolve.ngstd
import numpy
import numpy.typing
import pyngcore.pyngcore
import typing
__all__ = ['ArnoldiSolver', 'BaseMatrix', 'BaseSparseMatrix', 'BaseVector', 'BlockMatrix', 'BlockSmoother', 'BlockVector', 'CGSolver', 'ChebyshevIteration', 'ConstEBEMatrix', 'CreateParallelVector', 'CreateVVector', 'CumulationOperator', 'DeviceBlockGaussSeidelD', 'DeviceBlockGaussSeidelF', 'DeviceBlockJacobiD', 'DeviceBlockJacobiF', 'DeviceCGSolver', 'DeviceDiagonalMatrixD', 'DeviceDiagonalMatrixF', 'DeviceScalarD', 'DeviceScalarExpr', 'DeviceScalarF', 'DeviceSparseCholeskyD', 'DeviceSparseCholeskyF', 'DeviceSparseMatrixD', 'DeviceSparseMatrixF', 'DeviceTFQMRSolver', 'DeviceVectorC', 'DeviceVectorD', 'DeviceVectorF', 'DiagonalMatrix', 'DoArchive', 'DofRange', 'DynamicVectorExpression', 'EigenValues_Preconditioner', 'Embedding', 'EmbeddingTranspose', 'ExtractTri', 'GMRESSolver', 'GetAvailableSolvers', 'IdentityMatrix', 'InnerProduct', 'IsMatrixSymmetric', 'KrylovSpaceSolver', 'LoggingMatrix', 'MSMPrecond', 'MemoryUsage', 'MultiVector', 'MultiVectorExpr', 'PARALLEL_STATUS', 'ParallelDofs', 'ParallelMatrix', 'PermutationMatrix', 'ProductMatrix', 'Projector', 'QMRSolver', 'QMRSolverC', 'QMRSolverD', 'Real2ComplexMatrix', 'RegisterInverseType', 'S_BaseMatrixC', 'S_BaseMatrixD', 'Scalar', 'ScaleMatrix', 'Smoother', 'SparseCholesky', 'SparseCholesky_c', 'SparseCholesky_d', 'SparseFactorization', 'SparseFactorizationCreator', 'SparseFactorizationInterface', 'SparseMatrixDynamic', 'SparseMatrixN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE', 'SparseMatrixN5ngbla3MatILi2ELi2EdEE', 'SparseMatrixN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE', 'SparseMatrixN5ngbla3MatILi3ELi3EdEE', 'SparseMatrixNSt3__17complexIdEE', 'SparseMatrixSymmetricN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE', 'SparseMatrixSymmetricN5ngbla3MatILi2ELi2EdEE', 'SparseMatrixSymmetricN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE', 'SparseMatrixSymmetricN5ngbla3MatILi3ELi3EdEE', 'SparseMatrixSymmetricNSt3__17complexIdEE', 'SparseMatrixSymmetricd', 'SparseMatrixSymmetricf', 'SparseMatrixVariableBlocks', 'SparseMatrixd', 'SparseMatrixf', 'SumMatrix', 'SymmetricBlockGaussSeidelPreconditioner', 'SymmetricGaussSeidelPreconditioner', 'TransposeMatrix', 'VecFormat']
class BaseMatrix:
    @staticmethod
    def GetDefaultInverseType() -> str:
        ...
    @staticmethod
    def SetDefaultInverseType(type: str) -> None:
        ...
    def AsVector(self) -> BaseVector:
        """
        Interprets the matrix values as a vector
        """
    def ColFormat(self) -> VecFormat:
        """
        what the operator knows about its col vectors
        """
    @typing.overload
    def CreateColVector(self) -> BaseVector:
        ...
    @typing.overload
    def CreateColVector(self, like: BaseVector) -> BaseVector:
        """
        col vector, open axes (scalar, device, ...) taken from the given vector
        """
    def CreateDeviceMatrix(self, fp32: bool = False) -> BaseMatrix:
        """
        matrix on the device; fp32 uploads sparse values and block-Jacobi inverses in single precision
        """
    def CreateMatrix(self) -> BaseMatrix:
        """
        Create matrix of same dimension and same sparsestructure
        """
    @typing.overload
    def CreateRowVector(self) -> BaseVector:
        ...
    @typing.overload
    def CreateRowVector(self, like: BaseVector) -> BaseVector:
        """
        row vector, open axes (scalar, device, ...) taken from the given vector
        """
    def CreateSparseMatrix(self) -> ...:
        ...
    def CreateVector(self, colvector: bool = False) -> BaseVector:
        ...
    def GetInverseType(self) -> str:
        ...
    def GetMemoryUsage(self) -> list:
        """
        memory held by the operator, one entry per storage block
        """
    def GetOperatorInfo(self) -> str:
        ...
    def Inverse(self, freedofs: pyngcore.pyngcore.BitArray = None, inverse: None | str | typing.Any = None, flags: pyngcore.pyngcore.Flags | None = None) -> BaseMatrix:
        """
        Calculate inverse of sparse matrix
        Parameters:
        
        freedofs : BitArray
          If set, invert only the rows/columns the matrix defined by the bit array, otherwise invert the whole matrix
        
        inverse : string
          Solver to use, allowed values are:
            sparsecholesky - internal solver of NGSolve for symmetric matrices
            umfpack        - solver by Suitesparse/UMFPACK (if NGSolve was configured with USE_UMFPACK=ON)
            pardiso        - PARDISO, either provided by libpardiso (USE_PARDISO=ON) or Intel MKL (USE_MKL=ON).
                             If neither Pardiso nor Intel MKL was linked at compile-time, NGSolve will look
                             for libmkl_rt in LD_LIBRARY_PATH (Unix) or PATH (Windows) at run-time.
        """
    def Mult(self, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultAdd(self, value: typing.SupportsFloat | typing.SupportsIndex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultAdd(self, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultScale(self, value: typing.SupportsFloat | typing.SupportsIndex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultScale(self, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultTrans(self, value: typing.SupportsFloat | typing.SupportsIndex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultTrans(self, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultTransAdd(self, value: typing.SupportsFloat | typing.SupportsIndex, x: BaseVector, y: BaseVector) -> None:
        ...
    @typing.overload
    def MultTransAdd(self, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex, x: BaseVector, y: BaseVector) -> None:
        ...
    def RowFormat(self) -> VecFormat:
        """
        what the operator knows about its row vectors
        """
    def SetInverseType(self, arg0: str) -> str:
        ...
    def ToDense(self) -> typing.Any:
        ...
    def Update(self) -> None:
        """
        Update matrix
        """
    def __add__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __iadd__(self, mat: BaseMatrix) -> None:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: BaseVector) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: MultiVector) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: ngsolve.bla.MatrixD) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.Any) -> None:
        ...
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    @typing.overload
    def __mul__(self, arg0: BaseVector) -> ...:
        ...
    @typing.overload
    def __mul__(self, arg0: MultiVector) -> MultiVectorExpr:
        ...
    def __neg__(self) -> BaseMatrix:
        ...
    def __radd__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> BaseMatrix:
        ...
    @typing.overload
    def __rmul__(self, value: typing.SupportsFloat | typing.SupportsIndex) -> BaseMatrix:
        ...
    @typing.overload
    def __rmul__(self, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> BaseMatrix:
        ...
    def __stats__(self, total: bool = True) -> tuple[int, int, int]:
        """
        return loads[bytes] / stores[bytes] / flops
        """
    def __str__(self) -> str:
        ...
    def __sub__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __timing__(self, runs: typing.SupportsInt | typing.SupportsIndex = 10) -> float:
        ...
    def matvec(self, arg0: BaseVector) -> BaseVector:
        ...
    def rmatvec(self, arg0: BaseVector) -> BaseVector:
        ...
    @property
    def H(self) -> BaseMatrix:
        """
        Return conjugate transpose of matrix (WIP, only partially supported)
        """
    @property
    def T(self) -> BaseMatrix:
        """
        Return transpose of matrix
        """
    @property
    def comm(self) -> pyngcore.pyngcore.MPI_Comm | None:
        ...
    @property
    def dtype(self) -> numpy.dtype[typing.Any]:
        ...
    @property
    def height(self) -> int:
        """
        Height of the matrix
        """
    @property
    def is_complex(self) -> bool:
        """
        is the matrix complex-valued ?
        """
    @property
    def is_symmetric(self) -> pyngcore.pyngcore.xbool:
        ...
    @property
    def local_mat(self) -> BaseMatrix:
        ...
    @property
    def nze(self) -> int:
        """
        number of non-zero elements
        """
    @property
    def shape(self) -> tuple[int, int]:
        ...
    @property
    def width(self) -> int:
        """
        Width of the matrix
        """
class BaseSparseMatrix(BaseMatrix):
    """
    sparse matrix of any type
    """
    def CreateBlockSmoother(self, blocks: typing.Any, parallel: bool = False, GS: bool = False) -> typing.Any:
        ...
    def CreateSmoother(self, freedofs: pyngcore.pyngcore.BitArray = None, GS: bool = False) -> typing.Any:
        ...
    def DeleteZeroElements(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> BaseMatrix:
        ...
    @property
    def inverse_flags(self) -> pyngcore.pyngcore.Flags:
        """
        flags passed to the inverse (direct solver) created for this matrix
        """
    @inverse_flags.setter
    def inverse_flags(self, arg1: pyngcore.pyngcore.Flags) -> None:
        ...
class BaseVector:
    def Add(self, vec: BaseVector, value: typing.Any) -> None:
        ...
    def Assign(self, vec: BaseVector, value: typing.Any) -> None:
        ...
    def Copy(self) -> BaseVector:
        """
        creates a new vector of same type, copy contents
        """
    def CreateDeviceVector(self, unified: bool = True, copy: bool = True) -> BaseVector:
        """
        creates a device-vector of the same type
        """
    def CreateScalar(self) -> Scalar:
        ...
    def CreateVector(self, copy: bool = False) -> BaseVector:
        """
        creates a new vector of same type, contents is undefined if copy is false
        """
    def CreateVectors(self, num: typing.SupportsInt | typing.SupportsIndex) -> list[BaseVector]:
        """
        creates a num new vector of same type, contents is undefined
        """
    def Cumulate(self) -> None:
        ...
    def Distribute(self) -> None:
        ...
    def FV(self) -> typing.Any:
        ...
    def GetFormat(self) -> VecFormat:
        """
        vector type as VecFormat
        """
    def GetParallelStatus(self) -> PARALLEL_STATUS:
        ...
    @typing.overload
    def InnerProduct(self, other: BaseVector, conjugate: bool = True) -> typing.Any:
        """
        Computes (complex) InnerProduct
        """
    @typing.overload
    def InnerProduct(self, other: BaseVector, scal: Scalar, conjugate: bool = True) -> None:
        """
        Computes (complex) InnerProduct
        """
    def Norm(self) -> float:
        """
        Calculate Norm
        """
    def Range(self, from: typing.SupportsInt | typing.SupportsIndex, to: typing.SupportsInt | typing.SupportsIndex) -> BaseVector:
        """
        Return values from given range
        """
    def Reshape(self, width: typing.SupportsInt | typing.SupportsIndex) -> ngsolve.bla.FlatMatrixD:
        ...
    def SetParallelStatus(self, stat: PARALLEL_STATUS) -> None:
        ...
    def SetRandom(self, seed: typing.SupportsInt | typing.SupportsIndex | None = None) -> None:
        ...
    def __add__(self, arg0: ...) -> ...:
        ...
    def __buffer__(self, flags):
        """
        Return a buffer object that exposes the underlying memory of the object.
        """
    @typing.overload
    def __getitem__(self, ind: typing.SupportsInt | typing.SupportsIndex) -> typing.Any:
        """
        Return value at given position
        """
    @typing.overload
    def __getitem__(self, inds: slice) -> BaseVector:
        """
        Return values at given position
        """
    @typing.overload
    def __getitem__(self, arg0: ngsolve.ngstd.IntRange) -> BaseVector:
        ...
    @typing.overload
    def __getitem__(self, arg0: DofRange) -> BaseVector:
        ...
    def __getstate__(self) -> tuple[int, bool, int, ngsolve.ngstd._MemoryView]:
        ...
    @typing.overload
    def __iadd__(self, vec: BaseVector) -> BaseVector:
        ...
    @typing.overload
    def __iadd__(self, vec: ...) -> BaseVector:
        ...
    @typing.overload
    def __iadd__(self, arg0: ...) -> BaseVector:
        ...
    @typing.overload
    def __imul__(self, value: typing.SupportsFloat | typing.SupportsIndex) -> BaseVector:
        ...
    @typing.overload
    def __imul__(self, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> BaseVector:
        ...
    @typing.overload
    def __imul__(self, arg0: Scalar) -> BaseVector:
        ...
    @typing.overload
    def __init__(self, size: typing.SupportsInt | typing.SupportsIndex, complex: bool = False, entrysize: typing.SupportsInt | typing.SupportsIndex = 1) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: ...) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None:
        ...
    @typing.overload
    def __isub__(self, vec: BaseVector) -> BaseVector:
        ...
    @typing.overload
    def __isub__(self, vec: ...) -> BaseVector:
        ...
    @typing.overload
    def __isub__(self, arg0: ...) -> BaseVector:
        ...
    @typing.overload
    def __itruediv__(self, value: typing.SupportsFloat | typing.SupportsIndex) -> BaseVector:
        ...
    @typing.overload
    def __itruediv__(self, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> BaseVector:
        ...
    def __len__(self) -> int:
        ...
    def __neg__(self) -> ...:
        ...
    def __release_buffer__(self, buffer):
        """
        Release the buffer object that exposes the underlying memory of the object.
        """
    def __repr__(self) -> str:
        ...
    @typing.overload
    def __rmul__(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> ...:
        ...
    @typing.overload
    def __rmul__(self, arg0: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> ...:
        ...
    @typing.overload
    def __rmul__(self, arg0: Scalar) -> ...:
        ...
    @typing.overload
    def __setitem__(self, ind: typing.SupportsInt | typing.SupportsIndex, value: typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        Set value at given position
        """
    @typing.overload
    def __setitem__(self, ind: typing.SupportsInt | typing.SupportsIndex, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        Set value at given position
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        Set value at given positions
        """
    @typing.overload
    def __setitem__(self, inds: slice, vec: BaseVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, inds: slice, vec: ...) -> None:
        ...
    @typing.overload
    def __setitem__(self, inds: DofRange, vec: ...) -> None:
        ...
    @typing.overload
    def __setitem__(self, range: ngsolve.ngstd.IntRange, value: typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        Set value for range of indices
        """
    @typing.overload
    def __setitem__(self, range: ngsolve.ngstd.IntRange, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        Set value for range of indices
        """
    @typing.overload
    def __setitem__(self, range: ngsolve.ngstd.IntRange, vec: BaseVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, ind: typing.SupportsInt | typing.SupportsIndex, vec: ngsolve.bla.FlatVectorD) -> None:
        ...
    @typing.overload
    def __setitem__(self, ind: typing.SupportsInt | typing.SupportsIndex, vec: ngsolve.bla.FlatVectorC) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: pyngcore.pyngcore.BitArray, arg1: BaseVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: pyngcore.pyngcore.BitArray, arg1: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def __str__(self) -> str:
        ...
    def __sub__(self, arg0: ...) -> ...:
        ...
    def copy(self) -> BaseVector:
        """
        creates a new vector of same type, copy contents (scipy compatibility)
        """
    @property
    def comm(self) -> pyngcore.pyngcore.MPI_Comm | None:
        ...
    @property
    def data(self) -> BaseVector:
        ...
    @data.setter
    def data(self, arg1: ...) -> None:
        ...
    @property
    def dtype(self) -> numpy.dtype[typing.Any]:
        ...
    @property
    def is_complex(self) -> bool:
        ...
    @property
    def local_vec(self) -> BaseVector:
        ...
    @property
    def size(self) -> int:
        ...
class BlockMatrix(BaseMatrix):
    def __getitem__(self, inds: tuple) -> BaseMatrix:
        """
        Return value at given position
        """
    def __init__(self, mats: collections.abc.Sequence[collections.abc.Sequence[BaseMatrix]]) -> None:
        """
        Make BlockMatrix with given array of matrices
        """
    @property
    def col_nblocks(self) -> int:
        ...
    @property
    def row_nblocks(self) -> int:
        ...
class BlockSmoother(BaseMatrix):
    """
    block Jacobi and block Gauss-Seidel smoothing
    """
    def Smooth(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt | typing.SupportsIndex = 1, patches: pyngcore.pyngcore.BitArray = None) -> None:
        """
        performs steps block-Gauss-Seidel iterations for the linear system A x = b.
        If patches is given (BitArray, one bit per block, size == number of blocks),
        only the marked blocks are updated; all other blocks are left untouched.
        """
    def SmoothBack(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt | typing.SupportsIndex = 1, patches: pyngcore.pyngcore.BitArray = None) -> None:
        """
        performs steps block-Gauss-Seidel iterations for the linear system A x = b in reverse order.
        Same patches semantics as Smooth.
        """
class BlockVector(BaseVector):
    def __getitem__(self, ind: typing.SupportsInt | typing.SupportsIndex) -> BaseVector:
        """
        Return block at given position
        """
    def __init__(self, vecs: collections.abc.Sequence[BaseVector]) -> None:
        """
        Makes BlockVector by given array of vectors
        """
    @property
    def nblocks(self) -> int:
        """
        number of blocks in BlockVector
        """
class ConstEBEMatrix(BaseMatrix):
    def __init__(self, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex, matrix: ngsolve.bla.MatrixD, col_ind: list, row_ind: list) -> None:
        ...
    @property
    def col_ind(self) -> ...:
        ...
    @property
    def mat(self) -> ngsolve.bla.FlatMatrixD:
        ...
    @property
    def row_ind(self) -> ...:
        ...
class CumulationOperator(BaseMatrix):
    def __init__(self, arg0: ParallelDofs) -> None:
        ...
class DeviceBlockGaussSeidelD(MSMPrecond):
    """
    block Gauss-Seidel on the gpu, fp64
    """
class DeviceBlockGaussSeidelF(MSMPrecond):
    """
    block Gauss-Seidel on the gpu, fp32
    """
class DeviceBlockJacobiD(BaseMatrix):
    """
    block-Jacobi preconditioner on the gpu, fp64
    """
class DeviceBlockJacobiF(BaseMatrix):
    """
    block-Jacobi preconditioner on the gpu, fp32
    """
class DeviceDiagonalMatrixD(BaseMatrix):
    """
    diagonal matrix on the gpu, fp64
    """
class DeviceDiagonalMatrixF(BaseMatrix):
    """
    diagonal matrix on the gpu, fp32
    """
class DeviceScalarD(Scalar):
    """
    scalar on the gpu, fp64
    """
    @staticmethod
    def Sqrt(*args, **kwargs):
        """
        (self: object) -> ngsolve.la.DeviceScalarExpr
        """
    @staticmethod
    def __add__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __mul__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __neg__(*args, **kwargs):
        """
        (self: object) -> ngsolve.la.DeviceScalarExpr
        """
    @staticmethod
    def __radd__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __rmul__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __rsub__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __rtruediv__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __sub__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __truediv__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    def Get(self) -> float:
        """
        value on the host, waits for the queue
        """
    def Set(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def __float__(self) -> float:
        ...
    def __init__(self, value: typing.SupportsFloat | typing.SupportsIndex = 0.0) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def expr(self) -> DeviceScalarExpr:
        ...
    @property
    def data(self) -> float:
        """
        assign an expression, a device scalar or a number
        """
    @data.setter
    def data(self, arg1: typing.Any) -> None:
        ...
class DeviceScalarExpr:
    """
    expression of device scalars, evaluated on assignment
    """
    @staticmethod
    def Sqrt(*args, **kwargs):
        """
        (self: object) -> ngsolve.la.DeviceScalarExpr
        """
    @staticmethod
    def __add__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __mul__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __neg__(*args, **kwargs):
        """
        (self: object) -> ngsolve.la.DeviceScalarExpr
        """
    @staticmethod
    def __radd__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __rmul__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __rsub__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __rtruediv__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __sub__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __truediv__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
class DeviceScalarF(Scalar):
    """
    scalar on the gpu, fp32
    """
    @staticmethod
    def Sqrt(*args, **kwargs):
        """
        (self: object) -> ngsolve.la.DeviceScalarExpr
        """
    @staticmethod
    def __add__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __mul__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __neg__(*args, **kwargs):
        """
        (self: object) -> ngsolve.la.DeviceScalarExpr
        """
    @staticmethod
    def __radd__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __rmul__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __rsub__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __rtruediv__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __sub__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    @staticmethod
    def __truediv__(*args, **kwargs):
        """
        (self: object, arg0: object) -> object
        """
    def Get(self) -> float:
        """
        value on the host, waits for the queue
        """
    def Set(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    def __float__(self) -> float:
        ...
    def __init__(self, value: typing.SupportsFloat | typing.SupportsIndex = 0.0) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def expr(self) -> DeviceScalarExpr:
        ...
    @property
    def data(self) -> float:
        """
        assign an expression, a device scalar or a number
        """
    @data.setter
    def data(self, arg1: typing.Any) -> None:
        ...
class DeviceSparseCholeskyD(BaseMatrix):
    """
    sparse Cholesky solver on the gpu, fp64
    """
    def __init__(self, factorization: BaseMatrix) -> None:
        ...
class DeviceSparseCholeskyF(BaseMatrix):
    """
    sparse Cholesky solver on the gpu, fp32
    """
    def __init__(self, factorization: BaseMatrix) -> None:
        ...
class DeviceSparseMatrixD(BaseMatrix):
    """
    csr matrix on the gpu, fp64
    """
class DeviceSparseMatrixF(BaseMatrix):
    """
    csr matrix on the gpu, fp32
    """
class DeviceVectorC(BaseVector):
    """
    vector on the gpu, complex fp64
    """
    def D2H(self) -> DeviceVectorC:
        """
        copy into a host-visible device vector
        """
    def WaitUntilCompleted(self) -> None:
        """
        wait until all queued kernels writing this vector are done
        """
    @typing.overload
    def __init__(self, size: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @typing.overload
    def __init__(self, vec: BaseVector) -> None:
        ...
    @property
    def __cuda_array_interface__(self) -> dict:
        """
        cuda array interface (cuda backend only), for cupy, numba, torch
        """
    @property
    def memtype(self) -> ngsolve.ngstd.MemType:
        ...
class DeviceVectorD(BaseVector):
    """
    vector on the gpu, fp64
    """
    def D2H(self) -> DeviceVectorD:
        """
        copy into a host-visible device vector
        """
    def WaitUntilCompleted(self) -> None:
        """
        wait until all queued kernels writing this vector are done
        """
    @typing.overload
    def __init__(self, size: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @typing.overload
    def __init__(self, vec: BaseVector) -> None:
        ...
    @property
    def __cuda_array_interface__(self) -> dict:
        """
        cuda array interface (cuda backend only), for cupy, numba, torch
        """
    @property
    def memtype(self) -> ngsolve.ngstd.MemType:
        ...
class DeviceVectorF(BaseVector):
    """
    vector on the gpu, fp32
    """
    def D2H(self) -> DeviceVectorF:
        """
        copy into a host-visible device vector
        """
    def WaitUntilCompleted(self) -> None:
        """
        wait until all queued kernels writing this vector are done
        """
    @typing.overload
    def __init__(self, size: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @typing.overload
    def __init__(self, vec: BaseVector) -> None:
        ...
    @property
    def __cuda_array_interface__(self) -> dict:
        """
        cuda array interface (cuda backend only), for cupy, numba, torch
        """
    @property
    def memtype(self) -> ngsolve.ngstd.MemType:
        ...
class DiagonalMatrix(BaseMatrix):
    def __init__(self, arg0: BaseVector) -> None:
        ...
class DofRange(ngsolve.ngstd.IntRange):
    pass
class DynamicVectorExpression:
    def CreateVector(self) -> BaseVector:
        """
        create vector
        """
    def Evaluate(self) -> BaseVector:
        """
        create vector and evaluate expression into it
        """
    def InnerProduct(self, arg0: BaseVector) -> float:
        ...
    def Norm(self) -> float:
        ...
    def __add__(self, arg0: DynamicVectorExpression) -> DynamicVectorExpression:
        ...
    @typing.overload
    def __init__(self, arg0: BaseVector) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.float64]) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.Annotated[numpy.typing.ArrayLike, numpy.complex128]) -> None:
        ...
    def __neg__(self) -> DynamicVectorExpression:
        ...
    @typing.overload
    def __rmul__(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> DynamicVectorExpression:
        ...
    @typing.overload
    def __rmul__(self, arg0: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> DynamicVectorExpression:
        ...
    def __sub__(self, arg0: DynamicVectorExpression) -> DynamicVectorExpression:
        ...
class Embedding(BaseMatrix):
    def __init__(self, height: typing.SupportsInt | typing.SupportsIndex, range: ngsolve.ngstd.IntRange, complex: bool = False) -> None:
        """
        Linear operator embedding a shorter vector into a longer vector
        """
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
class EmbeddingTranspose(BaseMatrix):
    def __rmatmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
class IdentityMatrix(BaseMatrix):
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, size: typing.SupportsInt | typing.SupportsIndex, complex: bool = False) -> None:
        ...
class KrylovSpaceSolver(BaseMatrix):
    def GetSteps(self) -> int:
        ...
    def SetAbsolutePrecision(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    @property
    def maxsteps(self) -> int:
        ...
    @maxsteps.setter
    def maxsteps(self, arg1: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @property
    def tol(self) -> float:
        ...
    @tol.setter
    def tol(self, arg1: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
class LoggingMatrix(BaseMatrix):
    def __init__(self, mat: BaseMatrix, label: str, logfile: str = 'stdout', comm: pyngcore.pyngcore.MPI_Comm | None = None) -> None:
        ...
class MSMPrecond(BaseMatrix):
    """
    smoother with forward and backward sweeps
    """
    def Smooth(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt | typing.SupportsIndex = 1) -> None:
        ...
    def SmoothBack(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt | typing.SupportsIndex = 1) -> None:
        ...
class MemoryUsage:
    """
    bytes held by one storage block of an object
    """
    def __repr__(self) -> str:
        ...
    @property
    def device(self) -> int:
        """
        bytes in device memory
        """
    @property
    def host(self) -> int:
        """
        bytes in host ram
        """
    @property
    def name(self) -> str:
        ...
    @property
    def owner(self) -> int:
        """
        address of the object holding the memory, 0 if unknown
        """
class MultiVector(MultiVectorExpr):
    def Append(self, arg0: BaseVector) -> None:
        ...
    def AppendOrthogonalize(self, vec: BaseVector, ipmat: ... = None, parallel: bool = True, iterations: typing.SupportsInt | typing.SupportsIndex = 2) -> typing.Any:
        """
        assumes that existing vectors are orthogonal, and orthogonalize new vector against existing vectors
        """
    def Expand(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        """
        deprecated, use Extend instead
        """
    def Extend(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @typing.overload
    def InnerProduct(self, other: MultiVector, conjugate: bool = True) -> typing.Any:
        ...
    @typing.overload
    def InnerProduct(self, other: BaseVector, conjugate: bool = True) -> typing.Any:
        ...
    @typing.overload
    def InnerProduct(self, other: MultiVectorExpr, conjugate: bool = True) -> typing.Any:
        ...
    def Orthogonalize(self, ipmat: ... = None) -> typing.Any:
        """
        Orthogonalize vectors by modified Gram-Schmidt, returns R-factor of QR decomposition (only ipmat version, for the moment)
        """
    @typing.overload
    def Replace(self, ind: typing.SupportsInt | typing.SupportsIndex, v2: BaseVector) -> None:
        ...
    @typing.overload
    def Replace(self, inds: collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex], mv2: MultiVector) -> None:
        ...
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex) -> BaseVector:
        ...
    @typing.overload
    def __getitem__(self, arg0: slice) -> MultiVector:
        ...
    @typing.overload
    def __getitem__(self, arg0: pyngcore.pyngcore.Array_I_S) -> MultiVector:
        ...
    @typing.overload
    def __getitem__(self, arg0: tuple[slice, slice]) -> MultiVector:
        ...
    def __getstate__(self) -> tuple[typing.Any]:
        ...
    @typing.overload
    def __init__(self, arg0: BaseVector, arg1: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: typing.SupportsInt | typing.SupportsIndex, arg2: bool) -> None:
        ...
    def __len__(self) -> int:
        ...
    @typing.overload
    def __mul__(self, arg0: ngsolve.bla.VectorD) -> ...:
        ...
    @typing.overload
    def __mul__(self, arg0: ngsolve.bla.VectorC) -> ...:
        ...
    @typing.overload
    def __mul__(self, arg0: ngsolve.bla.MatrixD) -> MultiVectorExpr:
        ...
    @typing.overload
    def __mul__(self, arg0: ngsolve.bla.MatrixC) -> MultiVectorExpr:
        ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: ...) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt | typing.SupportsIndex, arg1: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: MultiVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: MultiVectorExpr) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex], arg1: MultiVector) -> None:
        ...
    @typing.overload
    def __setitem__(self, arg0: collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex], arg1: MultiVectorExpr) -> None:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    @property
    def data(self) -> MultiVector:
        ...
    @data.setter
    def data(self, arg1: MultiVectorExpr) -> None:
        ...
class MultiVectorExpr:
    def Evaluate(self) -> ...:
        ...
    def InnerProduct(self, arg0: typing.Any) -> typing.Any:
        ...
    @typing.overload
    def Scale(self, arg0: ngsolve.bla.VectorD) -> MultiVectorExpr:
        ...
    @typing.overload
    def Scale(self, arg0: ngsolve.bla.VectorC) -> MultiVectorExpr:
        ...
    def __add__(self, arg0: MultiVectorExpr) -> MultiVectorExpr:
        ...
    def __neg__(self) -> MultiVectorExpr:
        ...
    @typing.overload
    def __rmul__(self, arg0: typing.SupportsFloat | typing.SupportsIndex) -> MultiVectorExpr:
        ...
    @typing.overload
    def __rmul__(self, arg0: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> MultiVectorExpr:
        ...
    def __sub__(self, arg0: MultiVectorExpr) -> MultiVectorExpr:
        ...
class PARALLEL_STATUS:
    """
    enum of possible parallel statuses
    
    Members:
    
      DISTRIBUTED
    
      CUMULATED
    
      NOT_PARALLEL
    """
    CUMULATED: typing.ClassVar[PARALLEL_STATUS]  # value = <PARALLEL_STATUS.CUMULATED: 1>
    DISTRIBUTED: typing.ClassVar[PARALLEL_STATUS]  # value = <PARALLEL_STATUS.DISTRIBUTED: 0>
    NOT_PARALLEL: typing.ClassVar[PARALLEL_STATUS]  # value = <PARALLEL_STATUS.NOT_PARALLEL: 2>
    __members__: typing.ClassVar[dict[str, PARALLEL_STATUS]]  # value = {'DISTRIBUTED': <PARALLEL_STATUS.DISTRIBUTED: 0>, 'CUMULATED': <PARALLEL_STATUS.CUMULATED: 1>, 'NOT_PARALLEL': <PARALLEL_STATUS.NOT_PARALLEL: 2>}
    @typing.overload
    def __eq__(self, other: PARALLEL_STATUS) -> bool:
        ...
    @typing.overload
    def __eq__(self, other: typing.SupportsInt | typing.SupportsIndex) -> bool:
        ...
    @typing.overload
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def __int__(self) -> int:
        ...
    @typing.overload
    def __ne__(self, other: PARALLEL_STATUS) -> bool:
        ...
    @typing.overload
    def __ne__(self, other: typing.SupportsInt | typing.SupportsIndex) -> bool:
        ...
    @typing.overload
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ParallelDofs:
    def Dof2Proc(self, dof: typing.SupportsInt | typing.SupportsIndex) -> pyngcore.pyngcore.FlatArray_I_S:
        ...
    def EnumerateGlobally(self, freedofs: pyngcore.pyngcore.BitArray = None) -> tuple[typing.Any, typing.Any]:
        ...
    def ExchangeProcs(self) -> pyngcore.pyngcore.FlatArray_I_S:
        ...
    def MasterDofs(self) -> pyngcore.pyngcore.BitArray:
        ...
    def Proc2Dof(self, proc: typing.SupportsInt | typing.SupportsIndex) -> pyngcore.pyngcore.FlatArray_I_S:
        ...
    @property
    def comm(self) -> pyngcore.pyngcore.MPI_Comm:
        ...
    @property
    def entrysize(self) -> int:
        ...
    @property
    def ndofglobal(self) -> int:
        """
        number of global degrees of freedom
        """
    @property
    def ndoflocal(self) -> int:
        """
        number of degrees of freedom
        """
class PermutationMatrix(BaseMatrix):
    def __init__(self, w: typing.SupportsInt | typing.SupportsIndex, ind: collections.abc.Sequence[typing.SupportsInt | typing.SupportsIndex]) -> None:
        ...
class ProductMatrix(BaseMatrix):
    @property
    def matA(self) -> BaseMatrix:
        ...
    @property
    def matB(self) -> BaseMatrix:
        ...
class Projector(BaseMatrix):
    @typing.overload
    def Project(self, arg0: BaseVector) -> BaseVector:
        """
        project vector inline
        """
    @typing.overload
    def Project(self, arg0: MultiVector) -> MultiVector:
        """
        project vector inline
        """
    def __init__(self, mask: pyngcore.pyngcore.BitArray, range: bool) -> None:
        """
        Linear operator projecting to true/false bits of BitArray mask, depending on argument range
        """
class QMRSolverC(BaseMatrix):
    pass
class QMRSolverD(BaseMatrix):
    pass
class Real2ComplexMatrix(BaseMatrix):
    def __init__(self, arg0: BaseMatrix) -> None:
        ...
class S_BaseMatrixC(BaseMatrix):
    """
    base sparse matrix
    """
class S_BaseMatrixD(BaseMatrix):
    """
    base sparse matrix
    """
class Scalar:
    def __str__(self) -> str:
        ...
class ScaleMatrix(BaseMatrix):
    @property
    def mat(self) -> BaseMatrix:
        ...
class Smoother(BaseMatrix):
    """
    Jacobi and Gauss-Seidel smoothing
    """
    def Smooth(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt | typing.SupportsIndex = 1) -> None:
        """
        performs one step Gauss-Seidel iteration for the linear system A x = b
        """
    def SmoothBack(self, x: BaseVector, b: BaseVector, steps: typing.SupportsInt | typing.SupportsIndex = 1) -> None:
        """
        performs one step Gauss-Seidel iteration for the linear system A x = b in reverse order
        """
class SparseCholesky(SparseFactorization):
    @staticmethod
    def Create(arg0: BaseSparseMatrix, arg1: pyngcore.pyngcore.BitArray) -> SparseCholesky:
        ...
class SparseCholesky_c(SparseFactorization):
    def __getstate__(self) -> tuple[list]:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class SparseCholesky_d(SparseFactorization):
    def __getstate__(self) -> tuple[list]:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
class SparseFactorization(BaseMatrix):
    @staticmethod
    def Creator(*args, **kwargs):
        """
        (arg0: object, **kwargs) -> ngsolve.la.SparseFactorizationCreator
        """
    def Smooth(self, arg0: BaseVector, arg1: BaseVector) -> None:
        """
        perform smoothing step (needs non-symmetric storage so symmetric sparse matrix)
        """
class SparseFactorizationCreator:
    def __call__(self, arg0: BaseMatrix, arg1: pyngcore.pyngcore.BitArray) -> typing.Any:
        ...
class SparseFactorizationInterface(BaseMatrix):
    def Analyze(self) -> None:
        ...
    def Factor(self) -> None:
        ...
    def GetInnerMatrix(self) -> BaseSparseMatrix:
        ...
    def Update(self) -> None:
        ...
    def __init__(self, mat: BaseSparseMatrix, freedofs: pyngcore.pyngcore.BitArray = None) -> None:
        ...
    @property
    def is_spd(self) -> bool:
        ...
    @property
    def is_symmetric(self) -> pyngcore.pyngcore.xbool:
        ...
    @property
    def is_symmetric_storage(self) -> bool:
        ...
class SparseMatrixDynamic(BaseMatrix):
    def __init__(self, arg0: BaseMatrix) -> None:
        ...
class SparseMatrixN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex) -> SparseMatrixd:
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self, sorted: bool = True) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> ngsolve.bla.Mat2C:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self: SparseMatrixd, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self: SparseMatrixNSt3__17complexIdEE, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: ngsolve.bla.Mat2C) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixN5ngbla3MatILi2ELi2EdEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex) -> SparseMatrixd:
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self, sorted: bool = True) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> ngsolve.bla.Mat2D:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self: SparseMatrixd, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self: SparseMatrixNSt3__17complexIdEE, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: ngsolve.bla.Mat2D) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex) -> SparseMatrixd:
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self, sorted: bool = True) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> ngsolve.bla.Mat3C:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self: SparseMatrixd, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self: SparseMatrixNSt3__17complexIdEE, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: ngsolve.bla.Mat3C) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixN5ngbla3MatILi3ELi3EdEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex) -> SparseMatrixd:
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self, sorted: bool = True) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> ngsolve.bla.Mat3D:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self: SparseMatrixd, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self: SparseMatrixNSt3__17complexIdEE, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: ngsolve.bla.Mat3D) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixNSt3__17complexIdEE(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(*args, **kwargs) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex) -> SparseMatrixd:
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self, sorted: bool = True) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> complex:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self: SparseMatrixd, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self, mat: SparseMatrixNSt3__17complexIdEE) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixSymmetricN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE(SparseMatrixN5ngbla3MatILi2ELi2ENSt3__17complexIdEEEE):
    pass
class SparseMatrixSymmetricN5ngbla3MatILi2ELi2EdEE(SparseMatrixN5ngbla3MatILi2ELi2EdEE):
    pass
class SparseMatrixSymmetricN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE(SparseMatrixN5ngbla3MatILi3ELi3ENSt3__17complexIdEEEE):
    pass
class SparseMatrixSymmetricN5ngbla3MatILi3ELi3EdEE(SparseMatrixN5ngbla3MatILi3ELi3EdEE):
    pass
class SparseMatrixSymmetricNSt3__17complexIdEE(SparseMatrixNSt3__17complexIdEE):
    pass
class SparseMatrixSymmetricd(SparseMatrixd):
    pass
class SparseMatrixSymmetricf(SparseMatrixf):
    pass
class SparseMatrixVariableBlocks(BaseMatrix):
    def __init__(self, arg0: BaseMatrix) -> None:
        ...
class SparseMatrixd(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(indi: pyngcore.pyngcore.Array_I_S, indj: pyngcore.pyngcore.Array_I_S, values: pyngcore.pyngcore.Array_D_S, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex) -> SparseMatrixd:
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self, sorted: bool = True) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> float:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self: ..., std: ..., std: ..., mat: ..., std: ..., std: ...) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SparseMatrixf(BaseSparseMatrix):
    """
    a sparse matrix in CSR storage
    """
    @staticmethod
    def CreateFromCOO(indi: pyngcore.pyngcore.Array_I_S, indj: pyngcore.pyngcore.Array_I_S, values: pyngcore.pyngcore.Array_F_S, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex) -> ...:
        ...
    @staticmethod
    def CreateFromElmat(col_ind: list, row_ind: list, matrices: list, h: typing.SupportsInt | typing.SupportsIndex, w: typing.SupportsInt | typing.SupportsIndex) -> SparseMatrixd:
        ...
    def COO(self) -> typing.Any:
        ...
    def CSR(self) -> typing.Any:
        ...
    def CreateTranspose(self, sorted: bool = True) -> BaseSparseMatrix:
        """
        Return transposed matrix
        """
    def __getitem__(self, pos: tuple) -> float:
        """
        Return value at given position
        """
    @typing.overload
    def __matmul__(self: SparseMatrixd, mat: SparseMatrixd) -> ...:
        ...
    @typing.overload
    def __matmul__(self: ..., std: ..., std: ..., mat: ..., std: ..., std: ...) -> BaseMatrix:
        ...
    @typing.overload
    def __matmul__(self, mat: BaseMatrix) -> BaseMatrix:
        ...
    def __setitem__(self, pos: tuple, value: typing.SupportsFloat | typing.SupportsIndex) -> None:
        """
        Set value at given position
        """
    @property
    def entrysizes(self) -> tuple[int, int]:
        ...
class SumMatrix(BaseMatrix):
    @property
    def matA(self) -> BaseMatrix:
        ...
    @property
    def matB(self) -> BaseMatrix:
        ...
class SymmetricBlockGaussSeidelPreconditioner(BaseMatrix):
    pass
class SymmetricGaussSeidelPreconditioner(BaseMatrix):
    pass
class TransposeMatrix(BaseMatrix):
    @property
    def mat(self) -> BaseMatrix:
        ...
class VecFormat:
    """
    Describes a vector type: size, scalar type, entry size, parallel, device, blocks. Axes an operator does not know stay open.
    """
    def CreateVector(self) -> ...:
        ...
    def Merge(self, arg0: VecFormat) -> VecFormat:
        ...
    def WithDefaults(self) -> VecFormat:
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, size: typing.SupportsInt | typing.SupportsIndex) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    @property
    def blocks(self) -> list[VecFormat]:
        ...
    @property
    def entrysize(self) -> typing.Any:
        ...
    @property
    def is_complex(self) -> bool:
        ...
    @property
    def is_device(self) -> bool:
        ...
    @property
    def is_parallel(self) -> bool:
        ...
    @property
    def scalar(self) -> typing.Any:
        ...
    @property
    def size(self) -> typing.Any:
        ...
def ArnoldiSolver(mata: BaseMatrix, matm: BaseMatrix, freedofs: pyngcore.pyngcore.BitArray, vecs: list, shift: typing.SupportsComplex | typing.SupportsFloat | typing.SupportsIndex = ..., inverse: str | None = None) -> ngsolve.bla.VectorC:
    """
    Shift-and-invert Arnoldi eigenvalue solver
    
    Solves the generalized linear EVP A*u = M*lam*u using an Arnoldi iteration for the 
    shifted EVP (A-shift*M)^(-1)*M*u = lam*u with a Krylow space of dimension 2*len(vecs)+1.
    len(vecs) eigenpairs with the closest eigenvalues to the shift are returned.
    
    Parameters:
    
    mata : ngsolve.la.BaseMatrix
      matrix A
    
    matm : ngsolve.la.BaseMatrix
      matrix M
    
    freedofs : nsolve.ngstd.BitArray
      correct degrees of freedom
    
    vecs : list
      list of BaseVectors for writing eigenvectors
    
    shift : object
      complex or real shift
    """
def ChebyshevIteration(mat: BaseMatrix = None, pre: BaseMatrix = None, steps: typing.SupportsInt | typing.SupportsIndex = 3, lam_min: typing.SupportsFloat | typing.SupportsIndex = 1, lam_max: typing.SupportsFloat | typing.SupportsIndex = 1) -> BaseMatrix:
    ...
def CreateParallelVector(pardofs: ParallelDofs, status: PARALLEL_STATUS) -> ...:
    ...
def CreateVVector(size: typing.SupportsInt | typing.SupportsIndex, complex: bool = False, entrysize: typing.SupportsInt | typing.SupportsIndex = 1) -> ...:
    ...
def DoArchive(arg0: ngsolve.ngstd.Archive, arg1: BaseMatrix) -> ngsolve.ngstd.Archive:
    ...
def EigenValues_Preconditioner(mat: BaseMatrix, pre: BaseMatrix, tol: typing.SupportsFloat | typing.SupportsIndex = 1e-10) -> ngsolve.bla.VectorD:
    """
    Calculate eigenvalues of pre * mat, where pre and mat are positive definite matrices.
    The typical usecase of this function is to calculate the condition number of a preconditioner.It uses the Lanczos algorithm and bisection for the tridiagonal matrix
    """
def ExtractTri(mat: BaseSparseMatrix, lower: bool = True) -> BaseSparseMatrix:
    """
    Extract lower or upper triangular part of matrix
    """
def GetAvailableSolvers() -> list:
    ...
def InnerProduct(x: typing.Any, y: typing.Any, **kwargs) -> typing.Any:
    """
    Computes InnerProduct of given objects
    """
def IsMatrixSymmetric(mat: BaseSparseMatrix, tol: typing.SupportsFloat | typing.SupportsIndex = 0.0) -> bool:
    """
    Check if sparse matrix is symmetric with given tolerance
    """
@typing.overload
def ParallelMatrix(mat: typing.Any = None, row_pardofs: typing.Any = None, col_pardofs: typing.Any = None, op: typing.Any = None) -> None:
    ...
@typing.overload
def ParallelMatrix(mat: typing.Any = None, pardofs: typing.Any = None, op: typing.Any = None) -> None:
    ...
def RegisterInverseType(arg0: str, arg1: typing.Any) -> None:
    ...
