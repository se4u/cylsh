#!/usr/bin/env python
'''
| Filename    : mwe_e2lsh.py
| Description : A minimum working exmaple demostrating the usage of cython binding of E2LSH
| Author      : Pushpendre Rastogi
| Created     : Tue Feb  9 14:15:27 2016 (-0500)
| Last-Updated: Tue Feb  9 14:30:12 2016 (-0500)
|           By: Pushpendre Rastogi
|     Update #: 3
'''
from cylsh import LSH
import numpy as np
LSH_OR_MIPS = 'lsh'
dataset = np.loadtxt('../sample_data/mnist1k.dts')
queryset = np.loadtxt('../sample_data/mnist1k.q')
R = 0.8
K = 2
p = 0.9
sample_query = dataset[1:3, :]
# Create LSH Database
optim_param = LSH.compute_optimal_parameters(
    R, p, dataset, sample_query, 22020096)
db = LSH.init_manually(optim_param, dataset)
# Query LSH Database
print db.query(queryset[6])
