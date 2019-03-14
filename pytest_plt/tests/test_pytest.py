# -*- coding: utf-8 -*-
"""The main test file that should be run on a regular basis.

The goal of this file is to test pytest_plt internals and run all other
test files with various invocations of pytest to ensure that all possible
ways of using this plugin are tested.

By default, if you call ``pytest`` while in this repository, only this
file will be run due to configuration in ``setup.cfg``. However, other
test files can be run manually by passing them to ``pytest``.
"""

import os

import pytest
from pytest_plt.plugin import Mock

pytest_plugins = ["pytester"]


def test_mock():
    mock = Mock()

    # __getitem__ and __call__ should both return another `Mock`
    assert isinstance(mock["item"], Mock)
    assert isinstance(mock(), Mock)

    # __mul__ with anything should produce 1.0
    assert mock * "Hi" == 1.0

    # __getattr__ with __file__ and __path__ return "/dev/null"
    assert mock.__file__ == "/dev/null"
    assert mock.__file__ == mock.__path__

    # __getattr__ with uppercase first letter returns a type
    assert mock.Type.__module__ == "pytest_plt.plugin"
    assert type(mock.Type) is type

    # __getattr__ with lowercase first letter should return a `Mock`
    assert isinstance(mock.foo, Mock)


def assert_all_passed(result):
    """Assert that all outcomes are 0 except for 'passed'.

    Also returns the number of passed tests.
    """
    outcomes = result.parseoutcomes()
    for outcome in outcomes:
        if outcome not in ("passed", "seconds"):
            assert outcomes[outcome] == 0
    return outcomes.get("passed", 0)


def saved_plots(result):
    """Get a list of all tests with saved plots."""
    saved = []
    for i, line in enumerate(result.outlines):
        if line.startswith(u"└"):
            test = result.outlines[i - 1].split(" ")[0]
            plot = line.split("'")[1]
            saved.append((test, plot))
    return saved


def run_test_plt(testdir, folders, run_args=("--plots",), ini_source=None):
    for i in range(1, len(folders)+1):
        testdir.mkpydir('/'.join(folders[:i]))

    file_path = testdir.copy_example("test_plt.py")
    file_path.rename('/'.join(folders + ["test_plt.py"]))

    if ini_source is not None:
        testdir.makeini(ini_source)

    result = testdir.runpytest("-v", *run_args)
    return result


def test_plt_no_plots(testdir):
    result = run_test_plt(testdir, ["package", "tests"], run_args=[])

    # All tests should pass
    n_passed = assert_all_passed(result)
    assert n_passed > 0

    # No plots should be created
    saved = saved_plots(result)
    assert len(saved) == 0
    path = str(testdir.tmpdir)
    assert not os.path.exists(os.path.join(path, "plots"))


def test_plt_plots(testdir):
    result = run_test_plt(testdir, ["package", "tests"])

    # All tests should pass
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        assert plot.startswith("plots/package.tests.")
        assert os.path.exists(plot)


@pytest.mark.parametrize('drop_len', [1, 3])
def test_filename_drop_prefix(testdir, drop_len):
    parts = ["package", "folder", "tests"]

    drop_parts = parts[:drop_len]
    ini_source = r"""
    [pytest]
    plt_filename_drop =
        """ + "".join(p + r"\." for p in drop_parts)

    result = run_test_plt(testdir, parts, ini_source=ini_source)

    # All tests should pass
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for test, plot in saved:
        test_parts = test.split('/')
        for part, test_part in zip(parts, test_parts):
            assert part == test_part

        test_parts = test_parts[drop_len:]
        assert plot == "plots/" + '.'.join(test_parts) + '.pdf'
        assert os.path.exists(plot)


def test_plots_dir(testdir):
    result = run_test_plt(testdir, ["package", "tests"],
                          run_args=["--plots", "myplotdir"])

    # All tests should pass
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        assert plot.startswith("myplotdir/package.tests.")
        assert os.path.exists(plot)
