# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

from optas.matrix import make_ddg_matrix
from optas.matrix import make_matrix
from optas.tree import make_ddg_tree
from optas.tree import make_leaf_table
from optas.tree import make_tree

def test_probs_dyadic():
    P_desired = [
        [0, 0, 1], # 1
        [0, 0, 1], # 1
        [0, 1, 1], # 3
        [0, 0, 1], # 1
        [0, 1, 0], # 2
    ]
    Ms, k, l = [1, 1, 3, 1, 2], 3, 3
    P = make_matrix(Ms, k, l)
    L = make_leaf_table(P)
    root = make_tree(0, k, l, [], L)

    assert P == P_desired

    assert root.right.label is None
    assert root.right.right.label == 3
    assert root.right.left.label == 5

    assert root.left.label is None
    assert root.left.left.label is None
    assert root.left.right.label is None

    assert root.left.right.right.label == 1
    assert root.left.right.left.label == 2
    assert root.left.left.right.label == 3
    assert root.left.left.left.label == 4

def test_probs_nondyadic_basic():
    P_desired = [
        [0, 0, 1, 1], # 3
        [1, 1, 0, 0], # 12
    ]
    Ms, k, l = [3, 12], 4, 0
    P = make_matrix(Ms, k, l)
    L = make_leaf_table(P)
    root = make_tree(0, k, l, [], L)

    assert P == P_desired

    assert root.right.label == 2
    assert root.right.left is None

    assert root.left.label is None
    assert root.left.right.label == 2

    assert root.left.left.label is None
    assert root.left.left.right.label == 1

    assert root.left.left.left.label is None
    assert root.left.left.left.right.label == 1
    assert root.left.left.left.left == root

def test_probs_nondyadic_two_back_edge():
    P_desired = [
        [0, 1, 0, 1], # 5/14
        [0, 1, 0, 1], # 5/14
        [0, 1, 0, 0], # 4/14
    ]
    Ms, k, l = [5, 5, 4], 4, 1

    P = make_matrix(Ms, k, l)
    L = make_leaf_table(P)
    root = make_tree(0, k, l, [], L)

    assert P == P_desired

    assert len(L) == 5
    assert L[6] == 1
    assert L[5] == 2
    assert L[4] == 3
    assert L[18] == 1
    assert L[17] == 2

    assert root.right.right.label == 1
    assert root.right.right.right is None
    assert root.right.right.left is None
    assert root.right.left.label == 2
    assert root.right.left.right is None
    assert root.right.left.left is None

    assert root.left.right.label == 3
    assert root.left.right.left is None
    assert root.left.right.right is None

    assert root.left.left.right.right.label == 1
    assert root.left.left.right.left.label == 2

    assert root.left.left.left.left == root.left
    assert root.left.left.left.right == root.right

def test_probs_nondyadic_three_back_edges():
    P_desired = [
        [0, 1, 0, 0, 1], # 8/28
        [0, 0, 1, 0, 1], # 5/28
        [0, 0, 1, 0, 1], # 5/28
        [0, 0, 1, 0, 1], # 5/28
        [0, 0, 1, 0, 1], # 5/28
    ]
    Ms, k, l = [8, 5, 5, 5, 5], 5, 2

    P = make_matrix(Ms, k, l)
    L = make_leaf_table(P)
    root = make_tree(0, k, l, [], L)

    assert P == P_desired

    assert len(L) == 10
    assert L[6] == 1

    assert L[12] == 2
    assert L[11] == 3
    assert L[10] == 4
    assert L[9] == 5

    assert L[38] == 1
    assert L[37] == 2
    assert L[36] == 3
    assert L[35] == 4
    assert L[34] == 5

    assert root.right.right.label == 1
    assert root.right.left.right.label == 2
    assert root.right.left.left.label == 3

    assert root.left.right.right.label == 4
    assert root.left.right.left.label == 5

    assert root.left.left.right.right.right.label == 1
    assert root.left.left.right.right.left.label == 2
    assert root.left.left.right.left.right.label == 3
    assert root.left.left.right.left.left.label == 4

    assert root.left.left.left.right.right.label == 5
    assert root.left.left.left.right.left.label is None
    assert root.left.left.left.right.left == root.right.left

    assert root.left.left.left.left.right == root.left.right
    assert root.left.left.left.left.left == root.left.left

def test_reduction_to_single_node():
    # An end-to-end test with automatic
    # reduction and so forth.
    P_desired = [
        [0, 0, 0, 0], # 0
        [1, 1, 1, 1], # 15
    ]
    Ms, k, l = [0, 15], 4, 0
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    root = make_ddg_tree(P, kp, lp)
    assert kp == 1
    assert lp == 0
    assert root.label == 1
    assert root.right is None
    assert root.left is None
