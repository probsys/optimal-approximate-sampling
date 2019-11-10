# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

"""Algorithm for generating random bits lazily, adapted from

    Optimal Discrete Uniform Generation from Coin Flips, and Applications
    Jérémie Lumbroso, April 9, 2013
    https://arxiv.org/abs/1304.1916
"""

import random

k = 32
word = 0
pos = 0

def flip():
    global pos
    global word
    if pos == 0:
        word = random.getrandbits(k)
        pos = k
    pos -= 1
    return (word & (1 << pos)) >> pos
