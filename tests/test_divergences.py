# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

import pytest

from optas.divergences import GENERATORS
from optas.divergences import KERNELS
from optas.divergences import LABELS
from optas.divergences import compute_divergence_generator
from optas.divergences import compute_divergence_kernel

from optas.tests.utils import allclose
from optas.tests.utils import get_random_dist

def disabled_test_f_divergences_graphical():
    import matplotlib.pyplot as plt
    import numpy
    fig, axes = plt.subplots(nrows=3, ncols=4)
    for g, ax in zip(GENERATORS, numpy.ravel(axes)):
        func = GENERATORS[g]
        label = LABELS[g]
        ts = numpy.linspace(1e-1, 2, 100)
        ys = [func(t) for t in ts]
        ax.plot(ts, ys)
        ax.set_title(label)
    fig.set_size_inches((18, 10))
    fig.set_tight_layout(True)
    plt.show()


@pytest.mark.parametrize('x', range(20))
def test_kernel_generator_agree(x):
    p = get_random_dist(20)
    q = get_random_dist(20)
    for k in KERNELS:
        try:
            div_kernel = compute_divergence_kernel(p, q, KERNELS[k])
            div_generator = compute_divergence_generator(p, q, GENERATORS[k])
            assert allclose(float(div_kernel), float(div_generator))
        except NotImplementedError:
            continue
