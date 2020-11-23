#!/usr/bin/env python

"""Example of finding optimal distribution given a fixed precision."""

from tempfile import NamedTemporaryFile
from fractions import Fraction
from collections import Counter

from optas.divergences import KERNELS
from optas.opt import get_optimal_probabilities
from optas.construct import construct_sample_ky_encoding
from optas.sample import sample_ky_encoding

from optas.writeio import write_sample_ky_encoding

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

# Write sampler to disk (for the C command-line interface).
with NamedTemporaryFile(delete=False) as f:
    write_sample_ky_encoding(enc, n, k, f.name)
    print('\nsampler written to: %s' % (f.name,))
    print('to generate %d samples in C, run this command from c/ directory:'
        % (num_samples,))
    print('$ ./mainc.opt 1 %d ky.enc %s' % (num_samples, f.name))
