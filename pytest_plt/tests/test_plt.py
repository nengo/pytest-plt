"""Test the plt fixture."""

import inspect
import sys

import numpy as np


def test_mock_iter(plt):
    fig = plt.figure()
    for i, ax in enumerate(fig.axes):
        assert False, "Mock object iterating forever"
    plt.saveas = None


def test_simple_plot(plt):
    plt.plot(np.linspace(0, 1, 20), np.linspace(0, 2, 20))


def test_bbox_extra_artists(plt):
    plt.plot(np.linspace(0, 1, 20), np.linspace(0, 2, 20), label="line")
    legend = plt.legend(loc='upper left', bbox_to_anchor=(1., 1.))
    plt.bbox_extra_artists = (legend,)


_fns = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
plot_tests = [_name for _name, _fn in _fns
              if _name.startswith('test_')
              and 'plt' in inspect.getfullargspec(_fn).args]
plot_tests.remove('test_mock_iter')
