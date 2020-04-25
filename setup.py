# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

import os
import re
import subprocess

# If some modules are not found, we use others, so no need to warn:
try:
    from setuptools import setup
    from setuptools import Extension
    from setuptools.command.build_py import build_py
    from setuptools.command.sdist import sdist
except ImportError:
    from distutils.cmd import Command
    from distutils.command.build_py import build_py
    from distutils.command.sdist import sdist
    from distutils.core import Extension
    from distutils.core import setup

def get_version():
    # Try to read the description from git.
    try:
        desc = subprocess.check_output(
            ['git', 'describe', '--dirty', '--long', '--match', 'v*'])
    # Fall back to reading a VERSION file.
    except Exception:
        if os.path.exists('VERSION'):
            with open('VERSION', 'r') as f:
                version = f.read().strip()
        else:
            # XXX Default to version v1.0.
            # assert False, 'Fatal error: cannot determine version.'
            version = '1.0'
        return version, version

    # git describe a commit using the most recent tag reachable from it.
    # Release tags start with v* (XXX what about other tags starting with v?)
    # and are of the form `v1.1.2`.
    #
    # The variable `desc` will be of the form v1.1.2-2-gb92bef6[-dirty]:
    # - verpart     v1.1.2
    # - revpart     2
    # - localpart   gb92bef6[-dirty]
    match = re.match(r'^v([^-]*)-([0-9]+)-(.*)$', desc.decode('utf-8'))
    assert match is not None
    verpart, revpart, localpart = match.groups()
    # Create a post version.
    if revpart > '0' or 'dirty' in localpart:
        # Local part may be g0123abcd or g0123abcd-dirty.
        # Hyphens not kosher here, so replace by dots.
        localpart = localpart.replace('-', '.')
        full_version = '%s.post%s+%s' % (verpart, revpart, localpart)
    # Create a release version.
    else:
        full_version = verpart

    # Strip the local part if there is one, to appease pkg_resources,
    # which handles only PEP 386, not PEP 440.
    if '+' in full_version:
        pkg_version = full_version[:full_version.find('+')]
    else:
        pkg_version = full_version

    # Sanity-check the result.  XXX Consider checking the full PEP 386
    # and PEP 440 regular expressions here?
    assert '-' not in full_version, '%r' % (full_version,)
    assert '-' not in pkg_version, '%r' % (pkg_version,)
    assert '+' not in pkg_version, '%r' % (pkg_version,)

    return pkg_version, full_version

PKG_VERSION, FULL_VERSION = get_version()
VERSION_PY = 'src/version.py'

def write_version_py(path):
    try:
        with open(path, 'rb') as f:
            version_old = f.read()
    except IOError:
        version_old = None
    version_new = '__version__ = %r\n' % (FULL_VERSION,)
    if version_old != version_new:
        print('writing %s' % (path,))
        with open(path, 'w') as f:
            f.write(version_new)
    with open('VERSION', 'w') as f:
        f.write('%s\n' % (PKG_VERSION,))

class local_build_py(build_py):
    def run(self):
        write_version_py(VERSION_PY)
        build_py.run(self)

# Make sure the VERSION file in the sdist is exactly specified, even
# if it is a development version, so that we do not need to run git to
# discover it -- which won't work because there's no .git directory in
# the sdist.
class local_sdist(sdist):
    def make_release_tree(self, base_dir, files):
        sdist.make_release_tree(self, base_dir, files)
        version_file = os.path.join(base_dir, 'VERSION')
        print('updating %s' % (version_file,))
        # Write to temporary file first and rename over permanent not
        # just to avoid atomicity issues (not likely an issue since if
        # interrupted the whole sdist directory is only partially
        # written) but because the upstream sdist may have made a hard
        # link, so overwriting in place will edit the source tree.
        with open(version_file + '.tmp', 'w') as f:
            f.write('%s\n' % (PKG_VERSION,))
        os.rename(version_file + '.tmp', version_file)

setup(
    name='discrete_sampling',
    version=PKG_VERSION,
    description='Optimal Approximate Sampling from Discrete Probability Distributions',
    url='https://github.com/probcomp/optimal-approximate-sampling',
    license='Apache-2.0',
    maintainer='Feras A. Saad',
    maintainer_email='fsaad@.mit.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    packages=[
        'discrete_sampling',
        'discrete_sampling.tests',
        'discrete_sampling.examples',
    ],
    package_dir={
        'discrete_sampling': 'src',
        'discrete_sampling.tests': 'tests',
        'discrete_sampling.examples': 'examples',
    },
    cmdclass={
        'build_py': local_build_py,
        'sdist': local_sdist,
    },
    package_data={
        'discrete_sampling': [
            'orderm2',
            'phi',
            '../c/*.c',
        ],
    },
    tests_require=['pytest', 'scipy']
)
