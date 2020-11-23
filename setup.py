# Copyright 2020 MIT Probabilistic Computing Project.
# See LICENSE.txt

import os
import re
from setuptools import setup

# Determine the version (hardcoded).
dirname = os.path.dirname(os.path.realpath(__file__))
vre = re.compile('__version__ = \'(.*?)\'')
m = open(os.path.join(dirname, 'src', '__init__.py')).read()
__version__ = vre.findall(m)[0]

setup(
    name='optas',
    version=__version__,
    description='Optimal Approximate Sampling from Discrete Probability Distributions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/probcomp/optimal-approximate-sampling',
    maintainer='Feras A. Saad',
    maintainer_email='fsaad@mit.edu',
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
    packages=[
        'optas',
        'optas.tests',
        'optas.examples',
    ],
    package_dir={
        'optas': 'src',
        'optas.tests': 'tests',
        'optas.examples': 'examples',
    },
    package_data={
        'optas': [
            'orderm2',
            'phi',
            '../c/*.c',
        ],
    },
    extras_require={
        'tests': ['pytest', 'scipy']
    }
)
