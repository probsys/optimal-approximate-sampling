# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

import pytest

from discrete_sampling.divergences import GENERATORS
from discrete_sampling.divergences import KERNELS
from discrete_sampling.divergences import LABELS
from discrete_sampling.divergences import compute_divergence_generator
from discrete_sampling.divergences import compute_divergence_kernel

from discrete_sampling.tests.utils import allclose
from discrete_sampling.tests.utils import get_random_dist

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
