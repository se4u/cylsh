# USAGE: cd to directory, run python setup.py build_ext --inplace
__author__ = "pushpendre"
from distutils.core import setup
from distutils.extension import Extension
from distutils.spawn import find_executable
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import os, numpy
macros=[]
compile_time_env = {}

if os.environ["DOMIPS"]=="-DPERFORM_NEYSHABUR_MIPS":
    compile_time_env["DOMIPS"]="yes"
else:
    compile_time_env["DOMIPS"]="no"

modules = [Extension("cylsh",
                     ["cylsh.pyx",
                      "lsh.pxd",
                      "../sources/NearNeighbors.cpp",
                      "../sources/BucketHashing.cpp",
                      "../sources/Geometry.cpp",
                      "../sources/LocalitySensitiveHashing.cpp",
                      "../sources/Random.cpp",
                      "../sources/Util.cpp",
                      "../sources/GlobalVars.cpp",
                      "../sources/SelfTuning.cpp",
                      ],
                     language = "c++",
                     libraries=["m"],
                     include_dirs=["../sources", numpy.get_include()],
                     define_macros=macros,
                     # library_dirs=[""],
                     # extra_compile_args=[""],
                     # extra_link_args=[""]
                     )]

for e in modules:
    e.cython_directives = {"embedsignature" : True}
    e.boundscheck=True
    e.overflowcheck=True
    
setup(name = "cylsh",
      ext_modules = cythonize(modules,
                            compile_time_env=compile_time_env,
                            ),
      cmdclass={"build_ext": build_ext}
      )

