from __future__ import division
from math import *
from scipy.special import erfc
from numpy import sqrt, pi, exp
sqr = lambda x: pow(x, 2)
W = 4


def computeP(w, c):
    """# RealT computeFunctionP(RealT w, RealT c){
    #   RealT x = w / c;
    #   return 1 - ERFC(x / M_SQRT2) - M_2_SQRTPI / M_SQRT2 / x * (1 - EXP(-SQR(x) / 2));
    """
    x = w / c
    M_SQRT2 = sqrt(2)
    M_2_SQRTPI = 2 / sqrt(pi)
    return 1 - erfc(x / M_SQRT2) - M_2_SQRTPI / M_SQRT2 / x * (1 - exp(-sqr(x) / 2))


def compute_M_for_ULSH(k, p):
    """
    # // Computes the parameter <m> of the algorithm, given the parameter
    # // <k> and the desired success probability <successProbability>. Only
    # // meaningful when functions <g> are interdependent (pairs of
    # // functions <u>, where the <m> functions <u> are each k/2-tuples of
    # // independent LSH functions).
    # IntT computeMForULSH(IntT k, RealT successProbability){
    #   ASSERT((k & 1) == 0); // k should be even in order to use ULSH.
    #   RealT mu = 1 - POW(computeFunctionP(PARAMETER_W_DEFAULT, 1), k / 2);
    #   RealT P = successProbability;
    #   RealT d = (1-mu)/(1-P)*1/LOG(1/mu) * POW(mu, -1/(1-mu));
    #   RealT y = LOG(d);
    #   IntT m = CEIL(1 - y/LOG(mu) - 1/(1-mu));
    #   while (POW(mu, m-1) * (1 + m * (1-mu)) > 1 - P){
    #     m++;
    #   }
    #   return m;
    # }
    >>> [compute_M_for_ULSH(e, 0.9) for e in xrange(2,26,2)]
    [4.0, 5.0, 7.0, 9.0, 11.0, 14.0, 18.0, 22.0, 28.0, 35.0, 44.0, 55.0]
    """
    mu = 1 - pow(computeP(W, 1), k / 2)
    d = (1 - mu) / (1 - p) * 1 / log(1 / mu) * pow(mu, -1 / (1 - mu))
    y = log(d)
    m = ceil(1 - y / log(mu) - 1 / (1 - mu))
    while pow(mu, m - 1) * (1 + m * (1 - mu)) > 1 - p:
        m += 1
    return m
if __name__ == "__main__":
    import sys
    k = int(sys.argv[1])
    p = float(sys.argv[2])
    print compute_M_for_ULSH(k, p)
