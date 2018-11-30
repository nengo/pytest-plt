def test_mock_iter(plt):
    fig = plt.figure()
    for i, ax in enumerate(fig.axes):
        assert False, "Mock object iterating forever"
    plt.saveas = None
