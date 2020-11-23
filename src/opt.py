# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

from .utils import argmin
from .utils import argmin2
from .utils import normalize_vector

def get_delta_error(Z, p, M, delta, kernel):
    assert delta in [-1, 1]
    if delta == -1 and M == 0:
        return float('inf')
    if delta == 1 and M == Z:
        return float('inf')
    v1 = kernel(p, (M+delta)/Z)
    v0 = kernel(p, M/Z)
    return v1 - v0

def get_initial_Ms(Z, p_target, kernel):
    Ms = [0] * len(p_target)
    for i, p in enumerate(p_target):
        Ms[i] = int(Z*p)
        if get_delta_error(Z, p, Ms[i], +1, kernel) < 0:
            Ms[i] += 1
    return tuple(Ms)

def find_optimal_indexes(errs_dec, errs_inc):
    # Find the indexes of the lowest cost decrements and increments.
    j_min_dec0, j_min_dec1 = argmin2(errs_dec)
    j_min_inc0, j_min_inc1 = argmin2(errs_inc)
    # Ensure optimal indexes are distinct (optimally).
    if j_min_dec0 != j_min_inc0:
        j_min_dec = j_min_dec0
        j_min_inc = j_min_inc0
    else:
        cost0 = errs_dec[j_min_dec0] + errs_inc[j_min_inc1]
        cost1 = errs_dec[j_min_dec1] + errs_inc[j_min_inc0]
        if cost0 <= cost1:
            j_min_dec = j_min_dec0
            j_min_inc = j_min_inc1
        else:
            j_min_dec = j_min_dec1
            j_min_inc = j_min_inc0
    assert j_min_inc != j_min_dec
    return j_min_dec, j_min_inc

def prune_initial_Ms(Z, p_target, Ms, kernel):
    Ms = list(Ms)
    # Compute cost of decrements and increments.
    errs_dec = [
        get_delta_error(Z, p, M, -1, kernel)
        for M, p in zip(Ms, p_target)
    ]
    errs_inc = [
        get_delta_error(Z, p, M, +1, kernel)
        for M, p in zip(Ms, p_target)
    ]
    # Find optimal indexes.
    j_min_dec, j_min_inc = find_optimal_indexes(errs_dec, errs_inc)
    # Begin the loop.
    MAXITER = len(p_target) + 1
    iters = 0
    while errs_dec[j_min_dec] + errs_inc[j_min_inc] < 0:
        # Apply the optimal move.
        Ms[j_min_dec] -= 1
        Ms[j_min_inc] += 1
        # Update the costs.
        errs_dec[j_min_dec] = get_delta_error(
            Z, p_target[j_min_dec], Ms[j_min_dec], -1, kernel)
        errs_inc[j_min_inc] = get_delta_error(
            Z, p_target[j_min_inc], Ms[j_min_inc], +1, kernel)
        # Update the optimal indexes.
        j_min_dec, j_min_inc = find_optimal_indexes(errs_dec, errs_inc)
        # Update the iteration counter.
        iters += 1
        # Fail if exceeded theoretical number of iterations.
        # Will fire in cases of severe numerical instability.
        if iters > MAXITER:
            assert False, 'Fatal error: pruning exceeding MAXITER.'
    return tuple(Ms)

def fix_shortfall(Z, p_target, Ms, kernel):
    Ms = list(Ms)
    shortfall = sum(Ms) - Z
    delta = 1 if shortfall < 0 else -1
    errs_delta = [
        get_delta_error(Z, p, M, delta, kernel)
        for M, p in zip(Ms, p_target)
    ]
    while shortfall != 0:
        j_min = argmin(errs_delta)
        Ms[j_min] += delta
        errs_delta[j_min] = get_delta_error(
            Z, p_target[j_min], Ms[j_min], delta, kernel)
        shortfall += delta
    assert sum(Ms) == Z
    return tuple(Ms)

def optimize_unorm_strict(Z, p_target, kernel):
    """Run the optimization algorithm (requires p_target > 0 element-wise)."""
    # STEP 1: Initial guess.
    Ms_initial = get_initial_Ms(Z, p_target, kernel)
    # STEP 2: Pruning.
    Ms_prune = prune_initial_Ms(Z, p_target, Ms_initial, kernel)
    # STEP 3: Making up shortfall
    Ms_opt = fix_shortfall(Z, p_target, Ms_prune, kernel)
    # Return the result.
    return Ms_opt

def optimize_unorm(Z, p_target, kernel):
    """Run the optimization algorithm."""
    # STEP 1: Filter out zeros.
    p_nonzero_idx_vals = [(i, p) for (i, p) in enumerate(p_target) if p > 0]
    p_nonzero_idx = [i for i, _p in p_nonzero_idx_vals]
    p_nonzero_vals = [p for _i, p in p_nonzero_idx_vals]
    # STEP 2: Get the solution on the non-zero elements.
    Ms_opt_trunc = optimize_unorm_strict(Z, p_nonzero_vals, kernel)
    # STEP 3: Pad the solution
    Ms_opt = [0] * len(p_target)
    for j, idx in enumerate(p_nonzero_idx):
        Ms_opt[idx] = Ms_opt_trunc[j]
    # Return the result.
    return tuple(map(int, Ms_opt))

def get_optimal_probabilities_strict(Z, p_target, kernel):
    """Return optimal Z-type approximation of p_target under f-divergence."""
    Ms = optimize_unorm_strict(Z, p_target, kernel)
    return normalize_vector(Z, Ms)

def get_optimal_probabilities(Z, p_target, kernel):
    """Return optimal Z-type approximation of p_target under f-divergence."""
    Ms = optimize_unorm(Z, p_target, kernel)
    return normalize_vector(Z, Ms)
