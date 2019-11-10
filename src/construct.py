# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

from discrete_sampling.matrix import make_ddg_matrix
from discrete_sampling.matrix import make_hamming_matrix
from discrete_sampling.matrix import make_hamming_vector

from discrete_sampling.utils import get_Zkl
from discrete_sampling.utils import get_binary_expansion_length
from discrete_sampling.utils import get_common_denominator
from discrete_sampling.utils import get_common_numerators

from discrete_sampling.packing import pack_tree
from discrete_sampling.tree import make_ddg_tree

def construct_sample_ky_encoding(p_target):
    P, k, l = construct_sample_ky_matrix(p_target)
    root = make_ddg_tree(P, k, l)
    enc = {}
    pack_tree(enc, root, 0)
    n = len(P)
    encoding = [enc[i] for i in range(len(enc))]
    return encoding, n, k

def construct_sample_ky_matrix(p_target):
    Z = get_common_denominator(p_target)
    k, l = get_binary_expansion_length(Z)
    Zkl = get_Zkl(k, l)
    Ms = get_common_numerators(Zkl, p_target)
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    return P, kp, lp

def construct_sample_ky_matrix_cached(p_target):
    P, k, l = construct_sample_ky_matrix(p_target)
    h = make_hamming_vector(P)
    T = make_hamming_matrix(P)
    return k, l, h, T
