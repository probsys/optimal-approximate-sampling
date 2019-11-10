# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

import os
import subprocess

from fractions import Fraction
from functools import reduce
from math import gcd
from math import log2

PATH = os.path.dirname(os.path.abspath(__file__))
ORDERM2 = os.path.join(PATH, 'orderm2')

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def get_common_denominator(probabilities):
    """Return least Z such that each probability is a multiple of 1/Z."""
    denominators = [p.denominator for p in probabilities]
    return reduce(lcm, denominators)

def get_common_numerators(Z, probabilities):
    """Return numerator of probabilities expresses in the common base Z."""
    return [int(Z*p) for p in probabilities]

def normalize_vector(Z, Ms):
    """Normalize list of Ms by Z."""
    assert all(0 <= M <= Z for M in Ms)
    assert sum(Ms) <= Z
    return [Fraction(M, Z) for M in Ms]

def get_k_bit_prefixes(k):
    """Return list of prefix lengths using k-bit precision."""
    return list(range(k, -1, -1))

def get_Zb(k, l):
    """Return Z for k-l length suffix."""
    assert 0 < k and 0 <= l <= k
    return pow(2, k-l) - 1*(l<k)

def get_Zkl(k, l):
    """Return Z for k-bit precision and prefix length l."""
    assert 0 < k and 0 <= l <= k
    return pow(2, k) - pow(2, l)*(l<k)

def argmin2(l):
    """Return the indexes of the smalles two items in l."""
    (j1, m1) = (-1, float('inf'))
    (j2, m2) = (-1, float('inf'))
    for ix, x in enumerate(l):
        if x <= m1:
            (j2, m2) = (j1, m1)
            (j1, m1) = (ix, x)
        elif x < m2:
            (j2, m2) = (ix, x)
    return (j1, j2)

def argmin(l):
    """Return in the index of the smallest item in l."""
    (j1, _j2) = argmin2(l)
    return j1

def bits_to_int(bits):
    sbits = ''.join(map(str, bits))
    return int(sbits, 2)

def randint(k, bitstream):
    bits = [next(bitstream) for i in range(k)]
    return bits_to_int(bits)

def orderm2(M):
    """Return the multiplicative of 2 modulo odd integer M."""
    output = subprocess.check_output([ORDERM2, '%d' % (M,)])
    result = output.split(b'\n')[-2]
    return int(result)

def get_binary_expansion_length(M):
    """Return the length of prefix and suffix of binary expansion of 1/M."""
    if M % 2 == 1:
        k = orderm2(M)
        return (k, 0)
    Mp = M >> 1
    w = 1
    while (Mp % 2) == 0:
        w += 1
        Mp = Mp >> 1
    if Mp == 1:
        k = w
        l = k
    else:
        kp = orderm2(Mp)
        k = kp + w
        l = w
    return (k, l)

def encode_binary(x, width):
    """Convert integer x to binary with at least width digits."""
    assert isinstance(x, int)
    xb = bin(x)[2:]
    if width == 0:
        assert x == 0
        return ''
    else:
        assert len(xb) <= width
        pad = width  - len(xb)
        return '0' * pad + xb


def frac_to_bits(M, k, l):
    # Returns binary expansion of M / Zkl
    assert 0 <= M < get_Zkl(k, l) or (k == 1 and l == 0)
    if l == k:
        x = M
        y = 0
    elif l == 0:
        x = 0
        y = M
    else:
        Zb = pow(2, k-l) - 1
        x = M//Zb
        y = M - Zb * x
    a = encode_binary(x, l)
    s = encode_binary(y, k-l)
    b = a + s
    return [int(i) for i in b]

def reduce_fractions(Ms, k, l):
    """Simplify (M/Zkl | M in Ms) to lowest terms."""
    Zkl = get_Zkl(k, l)
    assert sum(Ms) == get_Zkl(k, l)
    if any(M==Zkl for M in Ms):
        Ms_prime = [M//Zkl for M in Ms]
        k_prime = 1
        l_prime = 0
        return (Ms_prime, k_prime, l_prime)
    if l == 0:
        return (Ms, k, l)
    if all(M%2 == 0 for M in Ms):
        Ms_prime = [M//2 for M in Ms]
        return reduce_fractions(Ms_prime, k-1, l-1)
    if all(M == Ms[0] for M in Ms):
        remainder = Zkl / Ms[0]
        base = log2(remainder)
        assert remainder == int(remainder)
        assert base == int(base)
        k_prime = int(base)
        l_prime = k_prime
        Ms_prime = [1] * len(Ms)
        return Ms_prime, k_prime, l_prime
    return Ms, k, l
