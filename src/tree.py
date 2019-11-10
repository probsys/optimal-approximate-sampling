# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

from math import log2

def make_leaf_table(P):
    N = len(P)
    k = len(P[0])
    table = {}
    current = 2
    for level in range(k):
        for row in range(N):
            if P[row][level] == 1:
                table[current] = row + 1
                current -= 1
        current = 2*current + 2
    return table

class Node(object):
    def __init__(self, index):
        self.index = index      # integer index in level order (root is 1).
        self.label = None       # integer label of outcome in {0,... n-1}.
        self.left = None        # pointer to left child node.
        self.right = None       # pointer to right child node.
        self.loc = None         # integer location in linear encoding.

def make_tree(index, k, l, ancestors, L):
    node = Node(index)
    if index in L:
        node.label = L[index]
    else:
        level = int(log2(index+1))
        index_lc = 2*index + 1
        index_rc = 2*index + 2

        # Internal nodes at level l are ancestors.
        if level == l:
            ancestors.append(node)

        # Build the right child.
        if level == k - 1 and index_rc not in L:
            assert node not in ancestors
            node.right = ancestors.pop(0)
        else:
            node.right = make_tree(index_rc, k, l, ancestors, L)

        # Build the left child.
        if level == k - 1 and index_lc not in L:
            assert node not in ancestors
            node.left = ancestors.pop(0)
        else:
            node.left = make_tree(index_lc, k, l, ancestors, L)

    return node

def make_ddg_tree(P, k, l):
    assert 0 < k and 0 <= l <= k
    if k == 1 and l == 0:
        root = Node(1)
        root.label = 1
        return root
    L = make_leaf_table(P)
    root = make_tree(0, k, l, [], L)
    return root
