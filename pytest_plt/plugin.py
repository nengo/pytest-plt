# -*- coding: utf-8 -*-

import errno
import inspect
import os
import re

from matplotlib import use as mpl_use
mpl_use('Agg')  # noqa: E402
from matplotlib import pyplot as mpl_plt
import pytest

from .compat import is_string


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:  # pragma: no cover
            raise


def pytest_addoption(parser):
    parser.addoption(
        '--plots', nargs='?', default=False, const=True,
        help='Save plots (can optionally specify a directory for plots).')


@pytest.hookimpl(hookwrapper=True)
def pytest_report_teststatus(report):
    outcome = yield
    category, shortletter, word = outcome.get_result()
    word = "PASSED" if word == "" else word
    if report.when == "teardown":
        for key, val in report.user_properties:
            if key == "plt_saved":
                outcome.force_result(
                    (category, shortletter, u"%s\n└─ Saved %r" % (word, val))
                )
            break


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
    def __init__(self, dirname, nodeid, filename_drop=None):
        self.dirname = dirname
        self.nodeid = nodeid
        self.saved = None
        self.filename_drop = [] if filename_drop is None else filename_drop

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
        filename = self.nodeid

        # flat filestructure (replace folders with dots in filename)
        filename = filename.replace(os.path.sep, '.')

        # drop parts of filename matching the given regexs
        for pattern in self.filename_drop:
            while True:
                match = re.search(pattern, filename)
                if not match:
                    break

                span = match.span()
                filename = filename[:span[0]] + filename[span[1]:]

        return "%s.%s" % (filename, ext)

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, type, value, traceback):
        raise NotImplementedError()

    def save(self, path):
        self.saved = path


class Plotter(Recorder):
    def __enter__(self):
        if self.record:
            self.plt = mpl_plt
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

            if len(self.plt.gcf().get_axes()) > 0:
                # tight_layout errors if no axes are present
                self.plt.tight_layout()

            self.save(os.path.join(self.dirname, self.plt.saveas))
            self.plt.close('all')

    def save(self, path):
        mkdir_p(os.path.dirname(path))
        savefig_kw = {'bbox_inches': 'tight'}
        if hasattr(self.plt, 'bbox_extra_artists'):
            savefig_kw['bbox_extra_artists'] = self.plt.bbox_extra_artists
        self.plt.savefig(path, **savefig_kw)
        super(Plotter, self).save(path)


def default_dirname_formatter(request, dirname):
    return dirname


plt_dirname_formatter = default_dirname_formatter


def set_plt_dirname_formatter(dirname_formatter):
    """Configure plot directory names with a custom Python function.

    This allows you to set a callable directory name formatter that will
    customize the plot directory for individual tests. For example, you can
    have the directory name depend on fixtures used by the test, to have tests
    grouped by fixture.

    Parameters
    ----------
    dirname_formatter : callable
        A callable function/class that takes two arguments: ``request`` and
        ``dirname``, and returns a new directory name as a string.

        ``request`` is a ``pytest`` fixture that provides information about the
        test function: https://docs.pytest.org/en/latest/reference.html#request

        ``dirname`` is the current proposed directory name as a string, based
        on the configuration files or command line argument. The formatter
        should modify or add to this directory name, as appropriate.
    """
    global plt_dirname_formatter

    if not callable(dirname_formatter):
        raise ValueError("dirname_formatter must be a callable object")

    argspec = inspect.getfullargspec(dirname_formatter)
    if len(argspec.args) != 2:
        raise ValueError("dirname_formatter must take two arguments: the "
                         "`request` fixture and a current `dirname` string")

    plt_dirname_formatter = dirname_formatter


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
    # read plt_filename_drop from .ini config file
    filename_drop = request.config.inicfg.get("plt_filename_drop", "")
    filename_drop = filename_drop.split('\n')
    filename_drop = [s for s in filename_drop if len(s) > 0]

    # read plt_dir from .ini config file
    ini_dirname = request.config.inicfg.get("plt_dirname", "plots")

    # read dirname
    dirname = request.config.getvalue("plots")
    if not is_string(dirname) and dirname:
        # no dirname provided with --plots argument, so use default
        dirname = ini_dirname
    elif not dirname:
        # --plots argument not provided, so disable plots
        dirname = None

    if dirname is not None:
        dirname = plt_dirname_formatter(request, dirname)

    plotter = Plotter(dirname, request.node.nodeid,
                      filename_drop=filename_drop)

    def _finalize():
        plotter.__exit__(None, None, None)
        if plotter.saved is not None:
            request.node.user_properties.append(("plt_saved", plotter.saved))

    request.addfinalizer(_finalize)
    return plotter.__enter__()
