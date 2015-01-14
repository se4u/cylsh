# USAGE: cd to directory, run python setup.py build_ext --inplace
__author__ = "pushpendre"
from distutils.core import setup
from distutils.extension import Extension
from distutils.spawn import find_executable
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import os

compiler = "g++"
if find_executable('icpc') is not None:
    compiler = "icpc"
COMP_OPT = "%s -fast -DREAL_FLOAT -DPERFORM_NEYSHABUR_MIPS"%compiler
os.environ["CC"]=COMP_OPT
os.environ["CXX"]=COMP_OPT
modules = [Extension("cylsh",
                     ["cylsh.pyx",
                      "lsh.pxd",
                      "NearNeighbors.cpp",
                      "BucketHashing.cpp",
                      "Geometry.cpp",
                      "LocalitySensitiveHashing.cpp",
                      "Random.cpp",
                      "Util.cpp",
                      "GlobalVars.cpp",
                      "SelfTuning.cpp",
                      ],
                     language = "c++",
                     libraries=["m"],
                     library_dirs=["/Applications/Canopy.app/appdata/canopy-1.1.0.1371.macosx-x86_64/Canopy.app/Contents/lib"],
                     # extra_compile_args=[""],
                     # extra_link_args=[""]
                     )]

for e in modules:
    e.cython_directives = {"embedsignature" : True}
    
setup(name = "cylsh",
    ext_modules = modules,
    cmdclass={"build_ext": build_ext})
