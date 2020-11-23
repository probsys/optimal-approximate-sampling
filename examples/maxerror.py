#!/usr/bin/env python

"""Example of finding optimal distribution given a maximum allowed error."""

from math import ceil
from math import log2

from optas.divergences import KERNELS
from optas.divergences import compute_divergence_kernel
from optas.opt import get_optimal_probabilities
from optas.tests.utils import allclose
from optas.utils import argmin
from optas.utils import get_Zkl


def find_optimal_approximation(p_target, kernel, maxerror, dyadic):
    """Return optimal approximation

    Inputs:
    - p_target : list of target probabilities
    - kernel   : name of f-divergence to use, see KERNELS from divergences.py
    - maxerror : maximum permitted approximation error
    - dyadic   : True if sum of weights must be a power of two.

    Returns:
    - p_approx : the optimal approximation
    - error    : the achieved error
    - Z        : the sum of weights
    """
    assert allclose(sum(p_target), 1)

    # These divergence measures require the approximate distribution
    # to have full support over the domain of the target distribution
    # in order to achieve a finite error.
    strict = kernel in ['kl', 'nchi2']
    n = len(p_target)

    # Initial error and precision k.
    error = float('inf')
    k = 1 if not strict else ceil(log2(n))

    # Keep doubling precision
    while maxerror < error:
        # Possible sum of weights for given precision k.
        Z_list = [pow(2, k)] if dyadic else [get_Zkl(k, l) for l in range(1, k+1)]
        if strict:
            Z_list = [Z for Z in Z_list if len(p_target) <= Z]

        # List of approximate distributions, one for each Z.
        p_approx_list = [
            get_optimal_probabilities(Z, p_target, KERNELS[kernel])
            for Z in Z_list
        ]

        # List of errors, one of for each approximate distribution
        error_list = [
            compute_divergence_kernel(p_target, p_approx, KERNELS[kernel])
            for p_approx in p_approx_list
        ]

        # Record the lowest error.
        i = argmin(error_list)
        p_approx = p_approx_list[i]
        error = error_list[i]
        Z = Z_list[i]
        k += 1

    return (p_approx, error, Z)

(p_approx, error, Z) = find_optimal_approximation(
    p_target=[.07, .91, .02],
    kernel='nchi2',
    maxerror=2**-10,
    dyadic=False)

print('optimal approximate distribution', p_approx)
print('achieved error', error)
