The code from this project was used for ["Sublinear Partition Estimation"](http://arxiv.org/abs/1508.01596), Pushpendre Rastogi, Benjamin Van Durme, arXiv:1508.01596 [stat.ML] (Preprint).

This project serves two purposes:

1. It provides bindings for the LSH cpp code that was released by
   Andoni in Python. Original code is at www.mit.edu/~andoni/LSH.
   (Note: Since they released their code in GPL, therefore this is also
   GPL)

   The idea is that once everything compiles and all python paths are
   set correctly one would be able to do the following
   ```
    >>> import cylsh;
    >>> import numpy as np
    >>> db=cylsh.LSH(0.9,
                     0.9,
                     np.asarray([[.1, .7, .7],
                                [.11, .69, .7]]),
                     np.asarray([[.1, .7, .7]]),
                     1e6);
    >>> print db.query(np.asarray([.1, .7, 0]))
    ```
   "this example comes from the target example_cython_api" in the Makefile
   But remember that if you compiled it as cython_binding_mips
   then you must use the mips class.
   
2. Neyshabur et. al. (2014)[1] presented a clever modification to E2LSH
   to perform Maximum Inner Product Search. The code change was really
   small and it only needed like 10 lines of change to the following
   files to implement. So I added a flag to perform that as well in the Makefile.
   ```
   E2LSH-0.1/sources/Geometry.h
   E2LSH-0.1/sources/LocalitySensitiveHashing.h
   E2LSH-0.1/sources/LocalitySensitiveHashing.cpp
   E2LSH-0.1/sources/NearNeighbors.cpp
   ```
   Basically if you compile the module as "cython_binding_mips" then even though
   the API remains the same but the algorithm compiled would change
   and we would start doing MIPS based queries. Note that the parameter
   R would not map exactly to something meaningful.
   

Run the following in order to make the cython_bindings and to test them.

1. make cython_binding_mips for  NeyShabur's Maximum Inner Product LSH,
   or make cython_binding_e2lsh for Euclidean distance LSH
   Note that MIPS and MIPS mean the same thing.

2. make test_cython_binding_mips or test_cython_binding_lsh


All the code needed for creating cython bindings is in sources_py.
Read the original manual for understanding the c++ code.
Read the diffs "git diff --name-only 0a490a0d0 HEAD" for the c++ and
.h file to understand the changes done to implement Neyshabur
et. al.'s algorithm

```
[1] @article{neyshabur2014alsh,
Title = {{On Symmetric and Asymmetric LSHs for Inner Product Search}},
Author = {{Neyshabur}, B. and {Srebro}, N.},
Journal = {ArXiv e-prints},
Month = oct,
Primaryclass = {stat.ML},
Year = 2014}
```
