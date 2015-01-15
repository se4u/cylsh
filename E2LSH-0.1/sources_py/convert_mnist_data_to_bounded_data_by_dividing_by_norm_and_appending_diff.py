import sys
import numpy as np
datafn=sys.argv[1]
mode=sys.argv[2]
max_norm=0
if mode=="train":
    with open(datafn, "rb") as f:
        for vec in f:
            vec=np.asarray([float(e) for e in vec.strip().split()])
            vec_l2norm=np.linalg.norm(vec)
            if vec_l2norm > max_norm:
                max_norm=vec_l2norm

with open(datafn, "rb") as f:
    for vec in open(datafn, "rb"):
        vec=np.asarray([float(e) for e in vec.strip().split()])
        if mode=="train":
            vec=vec/max_norm
        elif mode=="query":
            vec=vec/np.linalg.norm(vec)
        else:
            raise ValueError
        sys.stdout.write(" ".join("%0.10f"%vec[i] for i in xrange(vec.shape[0])))
        sys.stdout.write(" %0.10f\n"%np.sqrt(max(0, 1.0-np.linalg.norm(vec)**2)))

