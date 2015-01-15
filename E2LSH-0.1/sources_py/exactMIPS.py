import sys
import numpy as np
data=np.asarray([[float(e) for e in row.strip().split()] for row in open(sys.argv[1])])
query=np.asarray([[float(e) for e in row.strip().split()] for row in open(sys.argv[2])])

for query_idx in xrange(query.shape[1]):
    sorted_mips=sorted(list(enumerate(np.dot(data, query[query_idx,:]).tolist())), key=lambda x: x[1], reverse=True)
    print [sorted_mips[i] for i in range(10)]
    import pdb; pdb.set_trace()
