#!/usr/bin/env bash
set -e -v  # exit immediately on error, and print each line as it executes

# This script runs the test suite on the emulator

NAME=$0
COMMAND=$1

if [[ "$COMMAND" == "install" ]]; then
    conda install --quiet numpy
    pip install -e ".[tests]"
elif [[ "$COMMAND" == "script" ]]; then
    coverage run -m pytest pytest_plt -v --durations 20 --color=yes
    coverage run -a -m pytest pytest_plt -v --durations 20 --color=yes --plots
    coverage report -m
elif [[ "$COMMAND" == "after_success" ]]; then
    eval "bash <(curl -s https://codecov.io/bash)"
elif [[ -z "$COMMAND" ]]; then
    echo "$NAME requires a command like 'install' or 'script'"
else
    echo "$NAME does not define $COMMAND"
fi

set +e +v  # reset options in case this is sourced
