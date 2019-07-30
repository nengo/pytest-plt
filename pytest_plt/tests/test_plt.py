"""Test the plt fixture."""

import numpy as np


def test_rectification(plt):
    """The test shown in the documentation.

    Included here to be extra sure that the example works when copy-pasted
    into a user's tests, and to easily generate the plot that we display
    in documentation.
    """
    values = list(range(-10, 11))
    rectified = [v if v > 0 else 0 for v in values]
    assert all(v >= 0 for v in rectified)
    plt.plot(values, label="Original")
    plt.plot(rectified, label="Rectified")
    plt.legend()
    # Use png to render easier in docs
    plt.saveas = "%s.png" % (plt.saveas[:-4],)


def test_mock_iter(plt):
    fig = plt.figure()
    for _ in enumerate(fig.axes):
        assert False, "Mock object iterating forever"
    plt.saveas = None


def test_simple_plot(plt):
    plt.plot(np.linspace(0, 1, 20), np.linspace(0, 2, 20))


def test_bbox_extra_artists(plt):
    plt.plot(np.linspace(0, 1, 20), np.linspace(0, 2, 20), label="line")
    legend = plt.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    plt.bbox_extra_artists = (legend,)


def test_saveas(plt):
    assert plt.saveas.endswith("saveas.pdf")
    plt.saveas = None
