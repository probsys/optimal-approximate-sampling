# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

from .utils import frac_to_bits
from .utils import get_Zkl
from .utils import reduce_fractions

# Algorithm 3.

def make_matrix(Ms, k, l):
    assert sum(Ms) == get_Zkl(k, l)
    return [frac_to_bits(M, k, l) for M in Ms]

def make_ddg_matrix(Ms, k, l):
    Ms_prime, kp, lp = reduce_fractions(Ms, k, l)
    P = make_matrix(Ms_prime, kp, lp) if (kp, lp) != (1, 0) else [[1]]
    return P, kp, lp

def make_hamming_vector(P):
    N, k = len(P), len(P[0])
    return [sum(P[r][c] for r in range(N)) for c in range(k)]

def make_hamming_matrix(P):
    N, k = len(P), len(P[0])
    T = [[-1 for c in range(k)] for r in range(N)]
    for c in range(k):
        d = 0
        for r in range(N):
            if P[r][c] == 1:
                T[d][c] = r
                d += 1
    return T
