#!/usr/bin/env bash
if [[ ! -e .ci/common.sh || ! -e pytest_plt ]]; then
    echo "Run this script from the root directory of this repository"
    exit 1
fi
source .ci/common.sh

# This script runs the test suite on the emulator

NAME=$0
COMMAND=$1

if [[ "$COMMAND" == "install" ]]; then
    exe conda install --quiet numpy matplotlib
    exe pip install "$PYTEST"
    exe pip install -e ".[tests]"
elif [[ "$COMMAND" == "script" ]]; then
    exe coverage run -m pytest pytest_plt -v --durations 20 --color=yes
    exe coverage run -a -m pytest pytest_plt -v --durations 20 --color=yes --plots
    exe coverage report -m
elif [[ "$COMMAND" == "after_success" ]]; then
    eval "bash <(curl -s https://codecov.io/bash)"
elif [[ -z "$COMMAND" ]]; then
    echo "$NAME requires a command like 'install' or 'script'"
else
    echo "$NAME does not define $COMMAND"
fi

exit "$STATUS"
