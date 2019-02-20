"""Test the plt fixture."""

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
