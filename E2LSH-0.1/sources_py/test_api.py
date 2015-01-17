from __future__ import division
import sys, cylsh
import numpy as np
def lin_scan(q, dataset, dist_fnc, reverse):
    dist = [dist_fnc(dataset[i], q) for i in xrange(dataset.shape[0])]
    return sorted(list(enumerate(dist)), key=lambda x: x[1], reverse=reverse)

LSH_OR_MIPS=sys.argv[1]
R = float(sys.argv[2])
dataset = np.loadtxt(sys.argv[3])
queryset= np.loadtxt(sys.argv[4])

seed = 1234
num_query_pnt = 10
np.random.seed(seed)
reverse=None
if LSH_OR_MIPS == "lsh":
    dist_fnc = lambda x,y: np.linalg.norm(x-y)
    reverse=False
elif LSH_OR_MIPS == "mips":
    dist_fnc = lambda x,y: np.dot(x,y)
    reverse=True
else:
    raise ValueError
indices = np.random.randint(dataset.shape[0], size=num_query_pnt)
sample_query = dataset[indices,:]
print "Building datasets now"

db = cylsh.LSH(R, 0.9, dataset, sample_query, 22020096)
for i in xrange(queryset.shape[0]):
    q = queryset[i]
    tmp=db.query(q)
    time_taken = tmp["time_taken"]
    lsh_nbrs = tmp["neighbors"]
    true_nbrs = lin_scan(q, dataset, dist_fnc, reverse)
    lsh_nbrs_with_dist = [(e, [_e[1] for _e in true_nbrs if e==_e[0]][0]) for e in lsh_nbrs]
    lsh_nbrs = [e[0] for e in sorted(lsh_nbrs_with_dist, key=lambda x: x[1], reverse=reverse)]
    # find I = intersection of lsh_nbrs and true_nbrs
    # Divide |I|/|lsh_nbrs| (=L)
    # print lsh_nbrs
    print "Total time for R-NN query at radius %0.6f (radius no. 0):\t%0.6f"%(R, time_taken)
    print "Query point %d: found %d NNs at distance %f (0th radius). First 10 NNs are:"%(i, len(lsh_nbrs), R)
    for _i in xrange(min(10, len(lsh_nbrs))):
        l=lsh_nbrs[_i]
        (rank, dist) = [(i_, e[1]) for i_,e in enumerate(true_nbrs) if e[0]==l][0]
        print "%0.9d\tDistance:%0.6f\tRank:%d\tTrueNbr:%0.6d"%(l, dist, rank+1, true_nbrs[_i][0])
