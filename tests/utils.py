# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

import random

from collections import Counter
from fractions import Fraction
from itertools import product
from math import isinf

from scipy.stats import chisquare

def get_chisquare_pval(p_target, samples):
    N = len(samples)
    f_expected = [int(N*p) for p in p_target]
    counts = Counter(samples)
    keys = sorted(set(samples))
    f_actual = [counts[k] for k in keys]
    return chisquare(f_expected, f_actual)[1]

def get_bitstrings(k):
    """Return all length-k binary strings."""
    tuples = product(*[(0,1) for _i in range(k)])
    strings = [''.join(map(str, t)) for t in tuples]
    return strings

def get_random_dist(n):
    numerators = [random.randint(1, n**2) for i in range(n)]
    Z = sum(numerators)
    return [Fraction(a, Z) for a in numerators]

def get_random_dist_zeros(n):
    numerators = [random.randint(0, n**2) for i in range(n)]
    n_zero = random.randint(1, n-1)
    numerators[:n_zero] = [0]*n_zero
    random.shuffle(numerators)
    Z = sum(numerators)
    return [Fraction(a, Z) for a in numerators]

def allclose(a, b, rtol=1e-5, atol=1e-8):
    if isinf(a) and isinf(b):
        return True
    return abs(a - b) <= (atol + rtol * abs(b))
