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

pytest_plugins = ["pytester"]


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
    result.assert_outcomes(passed=3)

    path = str(testdir.tmpdir)
    assert not os.path.exists(os.path.join(path, "plots"))


def test_plt_plots(testdir):
    testdir.mkpydir("package")
    testdir.mkpydir("package/tests")
    file_path = testdir.copy_example("test_plt.py")
    file_path.rename("package/tests/test_plt.py")

    result = testdir.runpytest("--plots")
    result.assert_outcomes(passed=3)

    plotdir = os.path.join(
        str(testdir.tmpdir), "plots", "package", "tests",
    )

    assert os.path.exists(os.path.join(
        plotdir, "test_plt.py::test_simple_plot.pdf",
    ))

    assert os.path.exists(os.path.join(
        plotdir, "test_plt.py::test_bbox_extra_artists.pdf",
    ))
