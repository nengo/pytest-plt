"""The main test file that should be run on a regular basis.

The goal of this file is to test pytest_plt internals and run all other
test files with various invocations of pytest to ensure that all possible
ways of using this plugin are tested.

By default, if you call ``pytest`` while in this repository, only this
file will be run due to configuration in ``setup.cfg``. However, other
test files can be run manually by passing them to ``pytest``.
"""

import os

from pytest_plt import Mock
import pytest_plt.tests.test_plt as test_plt

pytest_plugins = ["pytester"]
pytest_outcomes = [
    'passed', 'skipped', 'failed', 'error', 'xfailed', 'xpassed']


def count_total_outcomes(outcomes):
    """Count the total number of outcomes (tests) in an outcome dict.

    The ``outcomes`` dict is obtained from ``RunResult.parseoutcomes()``.

    ``outcomes`` dict can have other values (e.g. "seconds"), so we can't just
    sum all values in the dict.
    """
    return sum(outcomes.get(outcome, 0) for outcome in pytest_outcomes)


def test_mock():
    mock = Mock()
    assert isinstance(mock["item"], Mock)
    assert mock * "Hi" == 1.0
    assert mock.__file__ == "/dev/null"
    assert mock.__file__ == mock.__path__
    assert mock.Type.__module__ == "pytest_plt"
    assert type(mock.Type) is type


def test_plt_no_plots(testdir):
    testdir.mkpydir("package")
    testdir.mkpydir("package/tests")
    file_path = testdir.copy_example("test_plt.py")
    file_path.rename("package/tests/test_plt.py")

    result = testdir.runpytest()
    outcomes = result.parseoutcomes()
    n_tests = count_total_outcomes(outcomes)
    assert outcomes['passed'] / n_tests == 1.0, "did not pass all tests"

    path = str(testdir.tmpdir)
    assert not os.path.exists(os.path.join(path, "plots"))


def test_plt_plots(testdir):
    testdir.mkpydir("package")
    testdir.mkpydir("package/tests")
    file_path = testdir.copy_example("test_plt.py")
    file_path.rename("package/tests/test_plt.py")

    result = testdir.runpytest("--plots")
    # import pdb; pdb.set_trace()
    outcomes = result.parseoutcomes()
    n_tests = count_total_outcomes(outcomes)
    assert outcomes['passed'] / n_tests == 1.0, "did not pass all tests"

    plotdir = os.path.join(
        str(testdir.tmpdir), "plots", "package", "tests",
    )

    for test_name in test_plt.plot_tests:
        assert os.path.exists(os.path.join(
            plotdir, "test_plt.py::%s.pdf" % test_name,
        ))
