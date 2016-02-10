from __future__ import division
import sys
import time
try:
    from cylsh import LSH
except:
    print "cylsh is not on PYTHONPATH. Try running the command PYTHONPATH=$PWD/sources_py python sources_py/test_api.py "
    exit(1)
import numpy as np
from compute_M_for_ULSH import compute_M_for_ULSH


def lin_scan(q, dataset, dist_fnc, reverse):
    dist = [dist_fnc(dataset[i], q) for i in xrange(dataset.shape[0])]
    return sorted(list(enumerate(dist)), key=lambda x: x[1], reverse=reverse)
try:
    LSH_OR_MIPS = sys.argv[1]
    dataset = np.loadtxt(sys.argv[2])
    queryset = np.loadtxt(sys.argv[3])
    R = float(sys.argv[4])
    K = int(sys.argv[5])
    p = float(sys.argv[6])
except:
    print "USING DEFAULT VALUES !!!"
    LSH_OR_MIPS = 'mips'
    dataset = np.loadtxt('../sample_data/mnist1k.dts')
    queryset = np.loadtxt('../sample_data/mnist1k.q')
    R = 0.8
    K = 2
    p = 0.9
assert LSH_OR_MIPS in ["lsh", "mips"]
# Note that the mnist1k.dts dataset contains vectors that have
# the exact same magnitude. This command demonstrates this.
# np.linalg.norm([np.linalg.norm(dataset[i]) - 1 for i in range(dataset.shape[0])])
# If we want to see the difference between using MIPS and
# E2LSH then we can randomly scale the data in the dataset and then
# the results between E2LSH and MIPS would be different
# For example after loading the dataset do this
print 'randomly rescaling the data to demonstrate the distance between LSH and mips'
import random
random.seed(1234)
np.random.seed(1234)
dataset = dataset * (np.random.rand(dataset.shape[0]) + 0.5)[:, None]

data_norms = np.linalg.norm(dataset, axis=1)
max_norm = max(data_norms)
dataset = dataset / max_norm
dataset = np.concatenate(
    (dataset, np.sqrt(1 - (data_norms / max_norm) ** 2)[:, None]), axis=1)

queryset = np.concatenate(
    (queryset / np.linalg.norm(queryset, axis=1)[:, None],
     np.zeros((queryset.shape[0], 1))),
    axis=1)

measure = ('distance' if LSH_OR_MIPS == 'lsh' else 'InnerProduct')
seed = 1234
num_query_pnt = 10
np.random.seed(seed)
reverse = None
dist_fnc, reverse = (((lambda x, y: np.linalg.norm(x - y)), False)
                     if LSH_OR_MIPS == 'lsh'
                     else ((lambda x, y: np.dot(x, y)), True))
indices = np.random.randint(dataset.shape[0], size=num_query_pnt)
sample_query = dataset[indices, :]
optim_param = LSH.compute_optimal_parameters(R, p,
                                             dataset, sample_query,
                                             22020096)
# M = compute_M_for_ULSH(K, p)
# optim_param = {'dimension': 300,
#                'parameterK': K,
#                'parameterL': M * (M - 1) / 2,
#                'parameterM': M,
#                'parameterR': R,
#                'parameterR2': R**2,
#                'parameterT': 1000,
#                'parameterW': 4.0,
#                'successProbability': 0.8999999761581421,
#                'typeHT': 3,
#                'useUfunctions': 1}
print "Building DB now"
st = time.time()
db = LSH.init_manually(optim_param, dataset)
print "time taken for building dataset %0.6f" % (time.time() - st)
time_taken = 0
for i in xrange(queryset.shape[0]):
    q = queryset[i]
    st = time.time()
    tmp = db.query(q)
    time_taken += (time.time() - st)
    lsh_nbrs = tmp["neighbors"]
    true_nbrs = lin_scan(q, dataset, dist_fnc, reverse)
    lsh_nbrs_with_dist = [(e, [_e[1] for _e in true_nbrs if e == _e[0]][0])
                          for e in lsh_nbrs]
    lsh_nbrs = [e[0]
                for e
                in sorted(lsh_nbrs_with_dist,
                          key=lambda x: x[1],
                          reverse=reverse)]
    # find I = intersection of lsh_nbrs and true_nbrs
    # Divide |I|/|lsh_nbrs| (=L)
    # print lsh_nbrs

    print "Query %d: Found %d NNs with %s %f. First 10 NNs are:" % (i, len(lsh_nbrs), measure, R)
    for _i in xrange(min(10, len(lsh_nbrs))):
        l = lsh_nbrs[_i]
        (rank, dist) = [(i_, e[1])
                        for i_, e
                        in enumerate(true_nbrs)
                        if e[0] == l][0]
        print "AssignedRank:% 3d\tId:% 9d\t%s:%0.6f\tTrueRank:%d\tTrueNbr:%0.6d"\
            % (_i + 1, l, measure, dist, rank + 1, true_nbrs[_i][0])
print "Average time taken %.6f" % time_taken
