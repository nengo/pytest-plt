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


def copy_all_tests(testdir, path):
    parts = path.strip("/").split("/")
    for i in range(1, len(parts) + 1):
        testdir.mkpydir('/'.join(parts[:i]))

    # Find all test files in the current folder, not including this one.
    # NB: If we add additional directories, this needs to change
    tests = [p for p in os.listdir(os.path.dirname(__file__))
             if p.startswith("test_") and p != "test_pytest.py"]
    for test in tests:
        test_path = testdir.copy_example(test)
        test_path.rename("%s/%s" % (path, test))


def saved_plots(result):
    """Get a list of all tests with saved plots."""
    saved = []
    for i, line in enumerate(result.outlines):
        if line.startswith(u"└"):
            test = result.outlines[i - 1].split(" ")[0]
            plot = line.split("'")[1]
            saved.append((test, plot))
    return saved


def test_plt_no_plots(testdir):
    copy_all_tests(testdir, "package/tests")

    # All tests should pass
    result = testdir.runpytest("-v")
    n_passed = assert_all_passed(result)
    assert n_passed > 0

    # No plots should be created
    saved = saved_plots(result)
    assert len(saved) == 0
    path = str(testdir.tmpdir)
    assert not os.path.exists(os.path.join(path, "plots"))


def test_plt_plots(testdir):
    copy_all_tests(testdir, "package/tests")

    # All tests should pass
    result = testdir.runpytest("-v", "--plots")
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        assert os.path.exists(plot)
        assert plot.startswith("plots/package.tests.")


@pytest.mark.parametrize(
    'prefix', ["package/", "package/folder/tests/"],
)
def test_filename_drop_prefix(testdir, prefix):
    """Tests removing strings from the start of a plot filename.

    This is the most common use case of filename_drop.
    """
    copy_all_tests(testdir, "package/folder/tests")
    testdir.makeini("\n".join([
        "[pytest]",
        "plt_filename_drop =",
        "    %s" % prefix.replace("/", r"\."),
    ]))

    # All tests should pass
    result = testdir.runpytest("-v", "--plots")
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed

    prefix_parts = prefix.strip('/').split('/')
    for test, plot in saved:
        test_parts = test.split('/')
        for prefix_part, test_part in zip(prefix_parts, test_parts):
            assert prefix_part == test_part

        test_parts = test_parts[len(prefix_parts):]
        assert (plot == "plots/%s.pdf" % '.'.join(test_parts)
                or plot == "plots/%s.png" % '.'.join(test_parts))
        assert os.path.exists(plot)


def test_filename_drop_within(testdir):
    """Tests removing strings within a plot filename, with complicated regexes.

    These are less common use cases of filename_drop.
    """
    copy_all_tests(testdir, "package/tests")
    testdir.makeini("\n".join([
        "[pytest]",
        "plt_filename_drop =",
        r"    package\.",
        # Matches the `test_` of the function name only
        r"    (?<=::)test_",
    ]))

    # All tests should pass
    result = testdir.runpytest("-v", "--plots")
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        assert plot.startswith("plots/tests.test_")
        colon_ix = plot.index("::")
        assert not plot[colon_ix:].startswith("::test_")


def test_plots_dir(testdir):
    copy_all_tests(testdir, "package/tests")
    result = testdir.runpytest("-v", "--plots", "myplotdir")
    # All tests should pass
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        assert plot.startswith("myplotdir/package.tests.")
        assert os.path.exists(plot)


def test_default_dir(testdir):
    copy_all_tests(testdir, "package/tests")
    testdir.makeini("\n".join([
        "[pytest]",
        "plt_dirname = mydefaultdir",
    ]))
    # test with default dir
    result = testdir.runpytest("-v", "--plots")
    n_passed = assert_all_passed(result)
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        assert plot.startswith("mydefaultdir/package.tests.")
        assert os.path.exists(plot)

    # test with default dir overwritten by command line
    result = testdir.runpytest("-v", "--plots", "myoverridedir")
    n_passed = assert_all_passed(result)
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        assert plot.startswith("myoverridedir/package.tests.")
        assert os.path.exists(plot)
