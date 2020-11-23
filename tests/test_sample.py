# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

import random

from collections import Counter

import pytest

from oas.matrix import make_ddg_matrix
from oas.matrix import make_hamming_matrix
from oas.matrix import make_hamming_vector
from oas.packing import pack_tree
from oas.tree import make_ddg_tree

from oas.sample import sample_ky_encoding
from oas.sample import sample_ky_matrix
from oas.sample import sample_ky_matrix_cached

import oas.flip

from oas.tests.utils import get_bitstrings
from oas.tests.utils import get_chisquare_pval

@pytest.mark.parametrize('seed', [10, 20, 100123])
def test_deterministic(seed):
    random.seed(seed)
    Ms, k, l = [0, 31], 5, 0
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    root = make_ddg_tree(P, kp, lp)
    encoding = {}
    pack_tree(encoding, root, 0)

    N_sample = 10000
    samples_mat = [sample_ky_matrix(P, kp, lp) for _i in range(N_sample)]
    samples_enc = [sample_ky_encoding(encoding) for _i in range(N_sample)]
    assert Counter(samples_mat)[1] == N_sample
    assert Counter(samples_enc)[1] == N_sample

@pytest.mark.parametrize('seed', [10, 20, 100123])
def test_nondetermistic(seed):
    random.seed(seed)
    Ms, k, l = [3, 12], 4, 0
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    root = make_ddg_tree(P, kp, lp)
    encoding = {}
    pack_tree(encoding, root, 0)

    N_sample = 10000
    samples_mat = [sample_ky_matrix(P, kp, lp) for _i in range(N_sample)]
    samples_enc = [sample_ky_encoding(encoding) for _i in range(N_sample)]

    pval_mat = get_chisquare_pval([3/15, 12/15], samples_mat)
    assert 0.05 < pval_mat

    pval_enc = get_chisquare_pval([3/15, 12/15], samples_enc)
    assert 0.05 < pval_enc

def test_sample_ky_matrix_cached():
    Ms, k, l = [3, 2, 1, 7, 2, 1], 4, 4
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    h = make_hamming_vector(P)
    T = make_hamming_matrix(P)

    samples = []
    oas.flip.k = 4
    for i in range(2**4):
        oas.flip.word = i
        oas.flip.pos = oas.flip.k
        result0 = sample_ky_matrix(P, kp, lp)

        oas.flip.word = i
        oas.flip.pos = oas.flip.k
        result1 = sample_ky_matrix_cached(kp, lp, h, T)

        assert result0 == result1
        samples.append(result0)

    counter = Counter(samples)
    assert counter[1] == 3
    assert counter[2] == 2
    assert counter[3] == 1
    assert counter[4] == 7
    assert counter[5] == 2
    assert counter[6] == 1
