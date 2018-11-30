"""
pytest_plt
==========

pytest fixtures for quickly creating Matplotlib plots in your tests.
"""

import errno
import inspect
import logging
import os
import re
import sys

import matplotlib
import numpy as np
import pytest

from .version import version as __version__

logger = logging.getLogger(__name__)
try:
    # Prevent output if no handler set
    logger.addHandler(logging.NullHandler())
except AttributeError:
    pass

__copyright__ = "2018-2019 pytest_plt contributors"
__license__ = "MIT license"

PY2 = sys.version_info[0] == 2


def is_string(obj):
    if PY2:
        string_types = (str, unicode)  # pylint: disable=undefined-variable
    else:
        string_types = (str,)
    return isinstance(obj, string_types)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def pytest_configure(config):
    matplotlib.use('Agg')


def pytest_addoption(parser):
    parser.addoption(
        '--plots', nargs='?', default=False, const=True,
        help='Save plots (can optionally specify a directory for plots).')


class Mock(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    def __getitem__(self, key):
        return Mock()

    def __iter__(self):
        return iter([])

    def __mul__(self, other):
        return 1.0

    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()


class Recorder(object):
    def __init__(self, dirname, nodeid):
        self.dirname = dirname
        self.nodeid = nodeid

    @property
    def record(self):
        return self.dirname is not None

    @property
    def dirname(self):
        return self._dirname

    @dirname.setter
    def dirname(self, _dirname):
        if _dirname is not None and not os.path.exists(_dirname):
            os.makedirs(_dirname)
        self._dirname = _dirname

    def get_filename(self, ext=""):
        return "%s.%s" % (self.nodeid, ext)

    def get_filepath(self, ext=""):
        if not self.record:
            raise ValueError("Cannot construct path when not recording")
        return os.path.join(self.dirname, self.get_filename(ext=ext))

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, type, value, traceback):
        raise NotImplementedError()


class Plotter(Recorder):
    def __enter__(self):
        if self.record:
            import matplotlib.pyplot as plt
            self.plt = plt
        else:
            self.plt = Mock()
        self.plt.saveas = self.get_filename(ext='pdf')
        return self.plt

    def __exit__(self, type, value, traceback):
        if self.record:
            if self.plt.saveas is None:
                del self.plt.saveas
                self.plt.close('all')
                return
            # Save it again in case the user changed it
            self.filename = self.plt.saveas
            del self.plt.saveas

            if len(self.plt.gcf().get_axes()) > 0:
                # tight_layout errors if no axes are present
                self.plt.tight_layout()

            savefig_kw = {'bbox_inches': 'tight'}
            if hasattr(self.plt, 'bbox_extra_artists'):
                savefig_kw['bbox_extra_artists'] = self.plt.bbox_extra_artists
                del self.plt.bbox_extra_artists

            figpath = os.path.join(self.dirname, self.filename)
            mkdir_p(os.path.dirname(figpath))
            self.plt.savefig(figpath, **savefig_kw)
            self.plt.close('all')


class Analytics(Recorder):
    DOC_KEY = 'documentation'

    def __init__(self, dirname, module_name, function_name):
        super(Analytics, self).__init__(dirname, module_name, function_name)

        self.data = {}
        self.doc = {}

    @staticmethod
    def load(path, module, function_name):
        modparts = module.split('.')
        modparts = modparts[1:]
        modparts.remove('tests')

        return np.load(os.path.join(path, "%s.%s.npz" % (
            '.'.join(modparts), function_name)))

    def __enter__(self):
        return self

    def add_data(self, name, data, doc=""):
        if name == self.DOC_KEY:
            raise ValueError("The name '{}' is reserved.".format(self.DOC_KEY))

        if self.record:
            self.data[name] = data
            if doc != "":
                self.doc[name] = doc

    def save_data(self):
        if len(self.data) == 0:
            return

        npz_data = dict(self.data)
        if len(self.doc) > 0:
            npz_data.update({self.DOC_KEY: self.doc})
        np.savez(self.get_filepath(ext='npz'), **npz_data)

    def __exit__(self, type, value, traceback):
        if self.record:
            self.save_data()


@pytest.fixture
def plt(request):
    """A pyplot-compatible plotting interface.

    Please use this if your test creates plots.

    This will keep saved plots organized in a simulator-specific folder,
    with an automatically generated name. savefig() and close() will
    automatically be called when the test function completes.

    If you need to override the default filename, set `plt.saveas` to
    the desired filename.
    """
    dirname = request.config.getvalue("plots")
    if not is_string(dirname):
        dirname = "plots"
    plotter = Plotter(dirname, request.node.nodeid)
    request.addfinalizer(lambda: plotter.__exit__(None, None, None))
    return plotter.__enter__()


@pytest.fixture
def data(request):
    """An object to store data for analysis.

    Please use this if you're concerned that accuracy or speed may regress.

    This will keep saved data organized in a simulator-specific folder,
    with an automatically generated name. Raw data (for later processing)
    can be saved with ``analytics.add_raw_data``; these will be saved in
    separate compressed ``.npz`` files. Summary data can be saved with
    ``analytics.add_summary_data``; these will be saved
    in a single ``.csv`` file.
    """
    dirname = request.config.getvalue("data")
    if not is_string(dirname):
        dirname = "data"
    analytics = Analytics(dirname, request.node.nodeid)
    request.addfinalizer(lambda: analytics.__exit__(None, None, None))
    return analytics.__enter__()
