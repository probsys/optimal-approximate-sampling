# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

import itertools

import pytest

from optas.divergences import KERNELS
from optas.divergences import compute_divergence_kernel
from optas.opt import get_optimal_probabilities

from optas.tests.utils import get_random_dist
from optas.tests.utils import get_random_dist_zeros
from optas.tests.utils import allclose

from optas.utils import argmin
from optas.utils import normalize_vector

def get_enumeration_tuples(Z, n):
    """Get all length-n tuples of nonnegative integers which sum to Z."""
    sequences = itertools.product(*[range(Z+1) for _i in range(n)])
    return filter(lambda s: sum(s)==Z, sequences)

def get_enumeration_opt(Z, n, p_target, allocations, kernel):
    """Run the enumeration algorithm (requires p_target > 0 element-wise)."""
    assert n == len(p_target)
    Ms_list = [normalize_vector(Z, Ms) for Ms in allocations]
    divs = [compute_divergence_kernel(p_target, Ms, kernel) for Ms in Ms_list]
    i_opt = argmin(divs)
    Ms_opt = Ms_list[i_opt]
    return Ms_opt

def check_solutions_match(Z, n, p_target, assignmemts, kernel):
    assert sum(p_target) == 1
    try:
        M_enum = get_enumeration_opt(Z, n, p_target, assignmemts, kernel)
        M_opt = get_optimal_probabilities(Z, p_target, kernel)
    except NotImplementedError:
        return True
    assert sum(M_enum) == 1
    assert sum(M_opt) == 1
    e_enum = compute_divergence_kernel(p_target, M_enum, kernel)
    e_opt = compute_divergence_kernel(p_target, M_opt, kernel)
    assert M_enum == M_opt or allclose(e_enum, e_opt)

@pytest.mark.parametrize('n', [2, 3, 4])
@pytest.mark.parametrize('k', [2, 3, 4])
def test_get_optimal_probabilities(n, k):
    Z = 2**(k)
    assignmemts = list(get_enumeration_tuples(Z, n))
    for kern in KERNELS:
        kernel = KERNELS[kern]
        p_target = get_random_dist(n)
        check_solutions_match(Z, n, p_target, assignmemts, kernel)

@pytest.mark.parametrize('n', [4, 5,])
@pytest.mark.parametrize('k', [2, 3, 4])
def test_get_optimal_probabilities__ci_(n, k):
    Z = 2**(k)
    assignmemts = list(get_enumeration_tuples(Z, n))
    for kern in KERNELS:
        kernel = KERNELS[kern]
        p_target = get_random_dist(n)
        check_solutions_match(Z, n, p_target, assignmemts, kernel)

def test_opt_zeros():
    Z = 100
    p_target = get_random_dist_zeros(50)
    idx_zero = [i for (i, p) in enumerate(p_target) if p==0]
    assert idx_zero
    for kern in KERNELS:
        try:
            M_opt = get_optimal_probabilities(Z, p_target, KERNELS[kern])
            assert [M_opt[i] == 0 for i in idx_zero]
        except NotImplementedError:
            continue

def test_opt_insufficient_precision():
    Z = 16
    p_target = get_random_dist_zeros(100)
    idx_zero = [i for (i, p) in enumerate(p_target) if p==0]
    assert idx_zero
    for kern in KERNELS:
        try:
            M_opt = get_optimal_probabilities(Z, p_target, KERNELS[kern])
            assert [M_opt[i] == 0 for i in idx_zero]
        except NotImplementedError:
            continue
        except Exception:
            # TODO: Handle this case more gracefully!
            # All sorts of errors arise when the list of errors
            # all all inf, since the solution values become negative.
            assert kern in ['nchi2', 'kl', 'jf']
