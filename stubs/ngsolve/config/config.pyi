from __future__ import annotations
__all__ = ['BUILD_STUB_FILES', 'BUILD_UMFPACK', 'CMAKE_CUDA_COMPILER', 'CMAKE_CXX_COMPILER', 'CMAKE_CXX_COMPILER_LAUNCHER', 'CMAKE_C_COMPILER', 'CMAKE_INSTALL_PREFIX', 'CMAKE_LINKER', 'ENABLE_UNIT_TESTS', 'INSTALL_DEPENDENCIES', 'MKL_LINK', 'NETGEN_DIR', 'NGSOLVE_COMPILE_DEFINITIONS', 'NGSOLVE_COMPILE_DEFINITIONS_PRIVATE', 'NGSOLVE_COMPILE_INCLUDE_DIRS', 'NGSOLVE_COMPILE_OPTIONS', 'NGSOLVE_INSTALL_DIR_BIN', 'NGSOLVE_INSTALL_DIR_CMAKE', 'NGSOLVE_INSTALL_DIR_INCLUDE', 'NGSOLVE_INSTALL_DIR_LIB', 'NGSOLVE_INSTALL_DIR_PYTHON', 'NGSOLVE_INSTALL_DIR_RES', 'NGSOLVE_VERSION', 'NGSOLVE_VERSION_GIT', 'NGSOLVE_VERSION_HASH', 'NGSOLVE_VERSION_MAJOR', 'NGSOLVE_VERSION_MINOR', 'NGSOLVE_VERSION_PATCH', 'NGSOLVE_VERSION_PYTHON', 'NGSOLVE_VERSION_TWEAK', 'USE_ACCELERATE_SPARSE', 'USE_CCACHE', 'USE_CUDA', 'USE_HYPRE', 'USE_LAPACK', 'USE_MKL', 'USE_MUMPS', 'USE_PARDISO', 'USE_UMFPACK', 'get_cmake_dir', 'get_compile_include_args', 'get_include_dir', 'get_include_dirs', 'get_library_dir', 'get_library_dirs', 'get_link_lib_args', 'get_netgen_include_dir', 'get_netgen_library_dir', 'is_python_package', 'version']
def _cmake_to_bool(s):
    ...
def _resolve_install_dir(install_dir, python_dir, anchor_file):
    ...
def get_cmake_dir():
    ...
def get_compile_include_args():
    """
    Compiler include flags (NGSolve + Netgen headers), formatted for the current platform.
    """
def get_include_dir():
    """
    Absolute path of the installed NGSolve headers.
    """
def get_include_dirs():
    """
    All include directories needed to compile against NGSolve (NGSolve and Netgen).
    """
def get_library_dir():
    """
    Absolute path of the installed NGSolve libraries.
    """
def get_library_dirs():
    """
    All library directories needed to link against NGSolve (NGSolve and Netgen).
    """
def get_link_lib_args():
    """
    Linker flags to link a shared library against NGSolve and Netgen, for the current platform.
    """
def get_netgen_include_dir():
    """
    Absolute path of the installed Netgen headers.
    """
def get_netgen_library_dir():
    """
    Absolute path of the installed Netgen libraries.
    """
BUILD_STUB_FILES: bool = True
BUILD_UMFPACK: bool = False
CMAKE_CUDA_COMPILER: str = ''
CMAKE_CXX_COMPILER: str = '/usr/bin/c++'
CMAKE_CXX_COMPILER_LAUNCHER: str = ''
CMAKE_C_COMPILER: str = '/usr/bin/cc'
CMAKE_INSTALL_PREFIX: str = '/Applications/Netgen.app'
CMAKE_LINKER: str = '/usr/bin/ld'
ENABLE_UNIT_TESTS: bool = False
INSTALL_DEPENDENCIES: bool = False
MKL_LINK: str = ''
NETGEN_DIR: str = '/Applications/Netgen.app'
NGSOLVE_COMPILE_DEFINITIONS: str = 'HAVE_NETGEN_SOURCES;HAVE_DLFCN_H;HAVE_CXA_DEMANGLE;USE_TIMEOFDAY;MSG_NOSIGNAL=0;USE_ACCELERATE_SPARSE;TCL;LAPACK;NGS_PYTHON;USE_UMFPACK'
NGSOLVE_COMPILE_DEFINITIONS_PRIVATE: str = ''
NGSOLVE_COMPILE_INCLUDE_DIRS: str = ''
NGSOLVE_COMPILE_OPTIONS: str = '$<$<COMPILE_LANGUAGE:CXX>:-std=c++20>;$<$<COMPILE_LANGUAGE:CXX>:-Wno-undefined-var-template;-Wno-vla-extension>;$<$<COMPILE_LANGUAGE:CXX>:-fcx-limited-range>;-DMAX_SYS_DIM=3'
NGSOLVE_INSTALL_DIR_BIN: str = 'Contents/MacOS'
NGSOLVE_INSTALL_DIR_CMAKE: str = 'Contents/Resources/CMake'
NGSOLVE_INSTALL_DIR_INCLUDE: str = 'Contents/Resources/include'
NGSOLVE_INSTALL_DIR_LIB: str = 'Contents/MacOS'
NGSOLVE_INSTALL_DIR_PYTHON: str = 'Contents/Resources/lib/python3.13/site-packages'
NGSOLVE_INSTALL_DIR_RES: str = 'Contents/Resources/share'
NGSOLVE_VERSION: str = '6.2.2608-38-g131ab3c20'
NGSOLVE_VERSION_GIT: str = 'v6.2.2608-38-g131ab3c20'
NGSOLVE_VERSION_HASH: str = 'g131ab3c20'
NGSOLVE_VERSION_MAJOR: str = '6'
NGSOLVE_VERSION_MINOR: str = '2'
NGSOLVE_VERSION_PATCH: str = '2608'
NGSOLVE_VERSION_PYTHON: str = '6.2.2608.post38.dev0'
NGSOLVE_VERSION_TWEAK: str = '38'
USE_ACCELERATE_SPARSE: bool = True
USE_CCACHE: bool = False
USE_CUDA: bool = False
USE_HYPRE: bool = False
USE_LAPACK: bool = True
USE_MKL: bool = False
USE_MUMPS: bool = False
USE_PARDISO: bool = False
USE_UMFPACK: bool = True
is_python_package: bool = False
version: str = 'v6.2.2608-38-g131ab3c20'
