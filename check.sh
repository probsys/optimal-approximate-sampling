#!/bin/sh

set -Ceu

: ${PYTHON:=python}

root=`cd -- "$(dirname -- "$0")" && pwd`

(
    set -Ceu
    cd -- "${root}"
    rm -rf build

    # Run Python tests.
    "$PYTHON" setup.py build
    if [ $# -eq 0 ]; then
        # By default run all tests.
        # Any test which uses this flag should end with __ci_() which
        # activates integration testing code path. If --integration is
        # not specified then a __ci_() test will either run as a crash test
        # or not run at all. (Use git grep '__ci_' to find these tests.)
        ./pythenv.sh "$PYTHON" -m pytest --pyargs optas
        # Run C crash test.
        cd c/ && make test
    elif [ ${1} = 'crash' ]; then
        ./pythenv.sh "$PYTHON" -m pytest -k 'not __ci_' --pyargs optas
    elif [ ${1} = 'release' ]; then
        # Make a release
        rm -rf dist
        "$PYTHON" setup.py sdist bdist_wheel
        twine upload --repository pypi dist/*
    else
        # If args are specified delegate control to user.
        ./pythenv.sh "$PYTHON" -m pytest "$@"
    fi
)
