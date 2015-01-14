# python setup.py build_ext --inplace
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import os
os.environ["CC"]="g++ -O3 -DREAL_FLOAT -DPERFORM_NEYSHABUR_MIPS"
# extra_compile_args=[""],
# extra_link_args=[""]
# language = "c++"
modules = [Extension("cylsh",["cylsh.pyx", "lsh.pxd"],
                     extra_link_args=["-lm "])]

for e in modules:
    e.cython_directives = {"embedsignature" : True}
    
setup(name = "cylsh",
    ext_modules = modules,
    cmdclass={"build_ext": build_ext})
