from __future__ import division
import sys, cylsh
import numpy as np
def lin_scan(q, dataset, dist_fnc):
    dist = [dist_fnc(dataset[i], q) for i in xrange(dataset.shape[0])]
    return sorted(list(enumerate(dist)), key=lambda x: x[1], reverse=True)

LSH_OR_MIPS=sys.argv[1]
dataset = np.loadtxt(sys.argv[2])
queryset= np.loadtxt(sys.argv[3])
seed = 1234
num_query_pnt = 10
np.random.seed(seed)

if LSH_OR_MIPS == "lsh":
    dist_fnc = lambda x,y: np.linalg.norm(x-y)
elif LSH_OR_MIPS == "mips":
    dist_fnc = lambda x,y: np.dot(x,y)
else:
    raise ValueError
indices = np.random.randint(dataset.shape[0], size=num_query_pnt)
sample_query = dataset[indices,:]
print "Building datasets now"

dbs = [cylsh.LSH(R, 0.9, dataset, sample_query, 1e9)
       for R in [6]]
for i in xrange(queryset.shape[0]):
    q = queryset[i]
    for db in dbs:
        tmp=db.query(q)
        lsh_neighbors = tmp["neighbors"]
        time_taken = tmp["time_taken"]
        true_nbrs = lin_scan(q, dataset, dist_fnc)
        # find I = intersection of lsh_neighbors and true_nbrs
        # Divide |I|/|lsh_neighbors| (=L)
        # print lsh_neighbors
        print [e[0] for e in true_nbrs[:len(lsh_neighbors)]]
        L = len(lsh_neighbors)
        I = len(set(lsh_neighbors).intersection(set(e[0] for e in true_nbrs)))
        print (I/L, I, L) if L != 0 else 0

