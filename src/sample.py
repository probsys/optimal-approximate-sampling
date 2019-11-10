# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

from .flip import flip

def sample_ky_encoding(enc):
    if len(enc) == 1:
        assert enc[0] == -1
        return 1

    c = 0
    while True:
        b = flip()
        c = enc[c + b]
        if enc[c] < 0:
            return -enc[c]

def sample_ky_matrix(P, k, l):
    if len(P) == 1:
        assert P[0][0] == 1
        return 1

    N = len(P)
    assert len(P[0]) == k
    assert 0 <= l <= k
    d = 0
    c = 0
    while True:
        b = flip()
        d = 2*d + (1 - b)
        for r in range(N):
            d = d - P[r][c]
            if d == - 1:
                return r + 1
        if c == k - 1:
            assert l < k-1
            c = l
        else:
            c = c + 1

def sample_ky_matrix_cached(k, l, h, T):
    if len(T) == 1:
        return 1
    assert len(T[0]) == k
    assert 0 <= l <= k
    d = 0
    c = 0
    while True:
        b = flip()
        d = 2*d + (1 - b)
        if d < h[c]:
            return T[d][c] + 1
        d = d - h[c]
        if c == k - 1:
            assert l < k-1
            c = l
        else:
            c = c + 1
