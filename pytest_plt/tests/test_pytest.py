# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

"""The main test file that should be run on a regular basis.

The goal of this file is to test pytest_plt internals and run all other
test files with various invocations of pytest to ensure that all possible
ways of using this plugin are tested.

By default, if you call ``pytest`` while in this repository, only this
file will be run due to configuration in ``setup.cfg``. However, other
test files can be run manually by passing them to ``pytest``.
"""

import pickle
import matplotlib.pyplot as plt
from pathlib import Path

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
        if outcome not in ("passed", "seconds", "warning"):
            assert outcomes[outcome] == 0
    return outcomes.get("passed", 0)


def copy_all_tests(testdir, path):
    parts = path.strip("/").split("/")
    for i in range(1, len(parts) + 1):
        testdir.mkpydir("/".join(parts[:i]))

    # Find all test files in the current folder, not including this one.
    # NB: If we add additional directories, this needs to change
    tests = [
        p
        for p in Path(__file__).parent.iterdir()
        if p.name.startswith("test_") and p.name != "test_pytest.py"
    ]
    for test in tests:
        test_path = testdir.copy_example(test.name)
        test_path.rename("%s/%s" % (path, test.name))


def saved_plots(result):
    """Get a list of all tests with saved plots."""
    saved = []
    for i, line in enumerate(result.outlines):
        if line.startswith("└"):
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
    assert not Path(path, "plots").exists()


def test_plt_plots(testdir):
    copy_all_tests(testdir, "package/tests")

    # All tests should pass
    result = testdir.runpytest("-v", "--plots")
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        p = Path(plot)
        assert p.exists()
        assert p.parts[0] == "plots"
        assert p.name.startswith("package.tests.")


@pytest.mark.parametrize("prefix", ["package/", "package/folder/tests/"])
def test_filename_drop_prefix(testdir, prefix):
    """Tests removing strings from the start of a plot filename.

    This is the most common use case of filename_drop.
    """
    copy_all_tests(testdir, "package/folder/tests")
    testdir.makeini(
        "\n".join(
            ["[pytest]", "plt_filename_drop =", "    %s" % prefix.replace("/", r"\.")]
        )
    )

    # All tests should pass
    result = testdir.runpytest("-v", "--plots")
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed

    prefix_parts = prefix.strip("/").split("/")
    for test, plot in saved:
        test_parts = test.split("/")
        for prefix_part, test_part in zip(prefix_parts, test_parts):
            assert prefix_part == test_part

        plot_name = ".".join(test_parts[len(prefix_parts) :]).replace(":", "-")
        path = Path(plot)
        assert path.parts[0] == "plots"
        assert path.stem == plot_name
        assert path.suffix in [".pdf", ".png", ".pickle"]
        assert path.exists()


def test_filename_drop_within(testdir):
    """Tests removing strings within a plot filename, with complicated regexes.

    These are less common use cases of filename_drop.
    """
    copy_all_tests(testdir, "package/tests")
    testdir.makeini(
        "\n".join(
            [
                "[pytest]",
                "plt_filename_drop =",
                r"    package\.",
                # Matches the `test_` of the function name only
                r"    (?<=--)test_",
            ]
        )
    )

    # All tests should pass
    result = testdir.runpytest("-v", "--plots")
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        assert Path(plot).parts[0] == "plots"
        assert Path(plot).name.startswith("tests.test_")
        colon_ix = plot.index("--")
        assert not plot[colon_ix:].startswith("--test_")


def test_plots_dir(testdir):
    copy_all_tests(testdir, "package/tests")
    result = testdir.runpytest("-v", "--plots", "myplotdir")
    # All tests should pass
    n_passed = assert_all_passed(result)

    # All plots should be created
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        path = Path(plot)
        assert path.parts[0] == "myplotdir"
        assert path.name.startswith("package.tests.")
        assert path.exists()


def test_default_dir(testdir):
    copy_all_tests(testdir, "package/tests")
    testdir.makeini("\n".join(["[pytest]", "plt_dirname = mydefaultdir"]))
    # test with default dir
    result = testdir.runpytest("-v", "--plots")
    n_passed = assert_all_passed(result)
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        path = Path(plot)
        assert path.parts[0] == "mydefaultdir"
        assert path.name.startswith("package.tests.")
        assert path.exists()

    # test with default dir overwritten by command line
    result = testdir.runpytest("-v", "--plots", "myoverridedir")
    n_passed = assert_all_passed(result)
    saved = saved_plots(result)
    assert 0 < len(saved) <= n_passed
    for _, plot in saved:
        path = Path(plot)
        assert path.parts[0] == "myoverridedir"
        assert path.name.startswith("package.tests.")
        assert path.exists()


def test_pickle_files_contain_a_figure(testdir):
    """ Verify that pickle files can be loaded and contain the correct
    figure. Th figure is tested by simply checking the number of axes.

    For the expected number of axes, see test_plt.py::test_saveas_pickle

    """
    copy_all_tests(testdir, "package/tests")

    result = testdir.runpytest("-v", "--plots")

    saved_files = [Path(plot) for _, plot in saved_plots(result)]
    saved_pickle_files = [path for path in saved_files if path.suffix == ".pickle"]

    for pickle_file in saved_pickle_files:
        try:
            pickle.load(open(pickle_file, "rb"))
            assert 6 == len(plt.gcf().axes)
        except pickle.UnpicklingError:
            assert False, "Could not read a pickled file {}".format(str(pickle_file))


def test_image_files_are_not_pickled(testdir):
    """ Verify that other output file formats are not mistakenly being
    pickled.
    """
    copy_all_tests(testdir, "package/tests")

    result = testdir.runpytest("-v", "--plots")

    saved_files = [Path(plot) for _, plot in saved_plots(result)]
    saved_img_files = [path for path in saved_files if path.suffix != ".pickle"]

    for img_file in saved_img_files:
        with pytest.raises(pickle.UnpicklingError):
            pickle.load(open(img_file, "rb"))
