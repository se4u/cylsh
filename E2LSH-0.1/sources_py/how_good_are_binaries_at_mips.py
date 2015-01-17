import sys
import numpy as np
dataset = np.loadtxt(sys.argv[1])
queryset = np.loadtxt(sys.argv[2])
def lin_scan(q, dataset):
    dist_fnc=lambda x,y: np.dot(x,y)
    dist = [dist_fnc(dataset[i], q) for i in xrange(dataset.shape[0])]
    return sorted(list(enumerate(dist)), key=lambda x: x[1], reverse=True)
begin=True
qp=-1
for row in open(sys.argv[3], "rb"):
    if begin:
        sys.stdout.write(row)
        if row.startswith("Total time"):
            begin=False
    else:
        if row.startswith("Total") or row.startswith("Mean"):
            print row,
            continue
        elif row.startswith("Query point"):
            qp+=1
            true_nbrs = lin_scan(queryset[qp,:], dataset)
            print row,
            continue
        else:
            nbr=int(row.strip().split()[0])
            true_rank = [i_ for i_,e in enumerate(true_nbrs) if e[0]==nbr]
            assert len(true_rank)==1
            print "%s\tRank:%d"%(row.strip(), true_rank[0]+1)
