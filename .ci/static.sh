#!/usr/bin/env bash
set -v  # print each line as it executes
shopt -s globstar

# This script runs the static style checks

NAME=$0
COMMAND=$1
STATUS=0  # used to exit with non-zero status if any check fails

if [[ "$COMMAND" == "install" ]]; then
    pip install ".[checks]"
elif [[ "$COMMAND" == "script" ]]; then
    flake8 pytest_plt || STATUS=1
    pylint docs pytest_plt || STATUS=1
    codespell -q 3 --skip="./build,./docs/_build" || STATUS=1
    # undo single-branch cloning
    git config --replace-all remote.origin.fetch +refs/heads/*:refs/remotes/origin/*
    git fetch origin master
    N_COMMITS=$(git rev-list --count HEAD ^origin/master)
    for ((i=0; i<N_COMMITS; i++)) do
        git log -n 1 --skip $i --pretty=%B | grep -v '^Co-authored-by:' | gitlint -vvv || STATUS=1
    done
elif [[ -z "$COMMAND" ]]; then
    echo "$NAME requires a command like 'install' or 'script'"
else
    echo "$NAME does not define $COMMAND"
fi
exit $STATUS

set +v  # reset options in case this is sourced
