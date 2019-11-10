# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

def pack_tree(enc, node, offset):
    assert node.loc is None
    node.loc = offset
    # Encode a leaf.
    if node.label is not None:
        enc[offset] = -node.label
        return offset + 1
    # Encode left child.
    if node.left.loc is not None:
        enc[offset] = node.left.loc
        w = offset + 2
    else:
        enc[offset] = offset + 2
        w = pack_tree(enc, node.left, offset+2)
    # Encode right child.
    if node.right.loc is not None:
        enc[offset + 1] = node.right.loc
    else:
        enc[offset + 1] = w
        w = pack_tree(enc, node.right, w)
    # Return the next offset.
    return w
