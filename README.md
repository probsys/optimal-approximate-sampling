# Optimal Approximate Sampling From Discrete Probability Distributions

This repository contains a prototype implementation of the optimal
sampling algorithms from:

> Feras A. Saad, Cameron E. Freer, Martin C. Rinard, and Vikash K. Mansinghka.
[Optimal Approximate Sampling From Discrete Probability
Distributions](https://doi.org/10.1145/3371104).
Proc. ACM Program. Lang. 4, POPL, Article 36 (January 2020), 33 pages.

## Installing

The C code for the main sampler is in the `c/` directory and the
Python 3 libraries are in the `src/` directory.

Only Python 3 is required to build and use the software (no dependencies).

    $ git clone https://github.com/probcomp/optimal-approximate-sampling
    $ cd optimal-approximate-sampling
    $ python setup.py install

To build the C sampler

    $ cd c && make all

## Usage

Please refer to [src/example.py](src/example.py) for a usage tutorial, shown
below as well

```python
import random

from tempfile import NamedTemporaryFile
from fractions import Fraction
from collections import Counter

from discrete_sampling.divergences import KERNELS
from discrete_sampling.opt import get_optimal_probabilities
from discrete_sampling.construct import construct_sample_ky_encoding
from discrete_sampling.sample import sample_ky_encoding

from discrete_sampling.writeio import write_sample_ky_encoding

# Target probability distribution.
p_target = [Fraction(1, 10), Fraction(3, 10), Fraction(4, 10), Fraction(2, 10)]

# Obtain optimal probabilities (Algorithm 3).
precision = 32
kernel = 'hellinger'
p_approx = get_optimal_probabilities(2**precision, p_target, KERNELS[kernel])

# Construct the sampler (Section 5).
enc, n, k = construct_sample_ky_encoding(p_approx)

# Run the sampler.
num_samples = 50000
samples = [sample_ky_encoding(enc) for _i in range(num_samples)]
counts = Counter(samples)

f_expect = [float(p) for p in p_target]
f_actual = [counts[i]/num_samples for i in sorted(counts.keys())]

print('generated %d samples' % (num_samples,))
print('average frequencies: %s' % (f_expect,))
print('sampled frequencies: %s' % (f_actual,))
```

This example script can be run directly:

    $ ./pythenv.sh python src/example.py

## Tests

To test the Python library and run a crash test in C (requires
[pytest](https://docs.pytest.org/en/latest/) and
[scipy](https://scipy.org/)):

    $ ./check.sh

## Experiments

The code for experiments in the POPL publication is available in a tarball
on the ACM Digital Library. Please refer to the online supplementary
material at https://doi.org/10.1145/3371104.
