# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

from optas.matrix import make_ddg_matrix
from optas.matrix import make_hamming_matrix
from optas.matrix import make_hamming_vector
from optas.matrix import make_matrix

from optas.utils import frac_to_bits

def test_make_matrix():
    Ms, k, l = [6, 6, 6, 6], 5, 3
    P = make_matrix(Ms, k, l)
    assert P[0] == P[1] == P[2] == P[3] == frac_to_bits(Ms[0], k, l)

    Ms, k, l = [6, 6, 6, 6], 5, 3
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    assert kp == 2
    assert lp == 2
    assert P[0] == P[1] == P[2] == P[3] == [0, 1]

def test_make_hamming_vector_matrix():
    P = [
        [1, 0, 0, 1],
        [0, 1, 1, 1],
        [1, 0, 0, 1],
        [0, 0, 0, 1],
    ]
    h = make_hamming_vector(P)
    assert h == [2, 1, 1, 4]
    T = make_hamming_matrix(P)
    assert T == [
        [ 0,  1,  1, 0],
        [ 2, -1, -1, 1],
        [-1, -1, -1, 2],
        [-1, -1, -1, 3],
    ]

    P = [
        [0, 1, 0, 0], # 4
        [0, 0, 0, 1], # 1
        [1, 0, 1, 0], # 10
        [0, 0, 0, 1], # 1
    ]
    h = make_hamming_vector(P)
    assert h == [1, 1, 1, 2]
    T = make_hamming_matrix(P)
    assert T == [
        [ 2,  0,  2,  1],
        [-1, -1, -1,  3],
        [-1, -1, -1,  -1],
        [-1, -1, -1,  -1],
    ]
