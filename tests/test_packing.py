# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

from optas.packing import pack_tree
from optas.tree import make_ddg_tree

def test_one_back_edge():
    k, l = 4, 0
    P = [
        [0, 0, 1, 1], # 3
        [1, 1, 0, 0], # 12
    ]

    root = make_ddg_tree(P, k, l)
    encoding = {}
    pack_tree(encoding, root, 0)

    back_edges = [b for a, b in encoding.items() if 0 <= b < a]
    assert back_edges == [0]

    leaves_three = sum(1 for b in encoding.values() if b == -1)
    assert leaves_three == 2

    leaves_twelve = sum(1 for b in encoding.values() if b == -2)
    assert leaves_twelve == 2
