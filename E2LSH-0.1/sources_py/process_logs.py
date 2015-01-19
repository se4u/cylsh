from __future__ import division
import sys
R=sys.argv[1].split()
K=sys.argv[2].split()
P=sys.argv[3].split()
def penalize_rank(rank):
    """ Penalize maximum if 1 is not present
    """
    penalty=0
    for i in range(1, 7):
        if i not in rank:
            penalty+=100/pow(2, i-1)
    return penalty
            
def calculate_mr_and_mt(f):
    prepare_to_read=False
    rank=[]
    penalty=[]
    for row in f:
        try:
            if row.startswith("Total"):
                time_taken=float(row.strip().split()[-1])
                if prepare_to_read:
                    penalty.append(penalize_rank(rank))
                    prepare_to_read=False
                rank=[]
            if prepare_to_read:
                rank.append(int(row.strip().split()[2][5:]))
                pass
            if row.startswith("Query"):
                prepare_to_read=True
        except:
            continue
    penalty.append(penalize_rank(rank))
    if len(penalty)!=100:
        print >>sys.stderr, "BAD FILE: ", f.name
        return None, None
    return time_taken, penalty

for r in R:
    for k in K:
        for p in P:
            #import pdb; pdb.set_trace()
            (mr, mt)=calculate_mr_and_mt(open("log/test_gauss_cython_mips~%s~%s~%s"%(r, k, p), "rb"))
            print r, k, p, mr, sum(mt) if mt is not None else mt
            
    
