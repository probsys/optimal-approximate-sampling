# Optimal Approximate Sampling From Discrete Probability Distributions

This repository contains a prototype implementation of the optimal
sampling algorithms from:

> Feras A. Saad, Cameron E. Freer, Martin C. Rinard, and Vikash K. Mansinghka.
[Optimal Approximate Sampling From Discrete Probability
Distributions](https://doi.org/10.1145/3371104).
_Proc. ACM Program. Lang._ 4, POPL, Article 36 (January 2020), 33 pages.

## Installing

The Python 3 library can be installed via pip:

    pip install optas

The C code for the main sampler is in the `c/` directory and the
Python 3 libraries are in the `src/` directory.

Only Python 3 is required to build and use the software from source.

    $ git clone https://github.com/probcomp/optimal-approximate-sampling
    $ cd optimal-approximate-sampling
    $ python setup.py install

To build the C sampler

    $ cd c && make all

## Usage

Please refer to the examples in the [examples](./examples) directory.
Given a fixed target distribution and error measure:

1. [./examples/sampling.py](./examples/sampling.py) shows an example of how
   to find an optimal distribution and sample from it, given a
   user-specified precision.

2. [./examples/maxerror.py](./examples/maxerror.py) shows an example of how
   to find an optimal distribution that uses the least possible precision
   and obtains an error that is less than a user-specified maximum
   allowable error.

These examples can be run directly as follows:

    $ ./pythenv.sh python examples/sampling.py
    $ ./pythenv.sh python examples/maxerror.py

## Tests

To test the Python library and run a crash test in C (requires
[pytest](https://docs.pytest.org/en/latest/) and
[scipy](https://scipy.org/)):

    $ ./check.sh

## Experiments

The code for experiments in the POPL publication is available in a tarball
on the ACM Digital Library. Please refer to the online supplementary
material at https://doi.org/10.1145/3371104.

## Citing

Please use the following BibTeX to cite this work.

    @article{saad2020sampling,
    title          = {Optimal approximate sampling from discrete probability distributions},
    author         = {Saad, Feras A. and Freer, Cameron E. and Rinard, Martin C. and Mansinghka, Vikash K.},
    journal        = {Proc. ACM Program. Lang.},
    volume         = 4,
    number         = {POPL},
    month          = jan,
    year           = 2020,
    pages          = {36:1--36:31},
    numpages       = 31,
    publisher      = {ACM},
    doi            = {10.1145/3371104},
    abstract       = {This paper addresses a fundamental problem in random variate generation: given access to a random source that emits a stream of independent fair bits, what is the most accurate and entropy-efficient algorithm for sampling from a discrete probability distribution $(p_1, \dots, p_n)$, where the output distribution $(\hat{p}_1, \dots, \hat{p}_n)$ of the sampling algorithm can be specified with a given level of bit precision? We present a theoretical framework for formulating this problem and provide new techniques for finding sampling algorithms that are optimal both statistically (in the sense of sampling accuracy) and information-theoretically (in the sense of entropy consumption). We leverage these results to build a system that, for a broad family of measures of statistical accuracy, delivers a sampling algorithm whose expected entropy usage is minimal among those that induce the same distribution (i.e., is ``entropy-optimal'') and whose output distribution $(\hat{p}_1, \dots, \hat{p}_n)$ is a closest approximation to the target distribution $(p_1, \dots, p_n)$ among all entropy-optimal sampling algorithms that operate within the specified precision budget. This optimal approximate sampler is also a closer approximation than any (possibly entropy-suboptimal) sampler that consumes a bounded amount of entropy with the specified precision, a class which includes floating-point implementations of inversion sampling and related methods found in many standard software libraries. We evaluate the accuracy, entropy consumption, precision requirements, and wall-clock runtime of our optimal approximate sampling algorithms on a broad set of probability distributions, demonstrating the ways that they are superior to existing approximate samplers and establishing that they often consume significantly fewer resources than are needed by exact samplers.},
    }
