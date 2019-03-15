"""
pytest_plt
==========

pytest fixtures for quickly creating Matplotlib plots in your tests.
"""

from .version import version as __version__

__copyright__ = "2018-2019 pytest_plt contributors"
__license__ = "MIT license"

from .plugin import plt, set_plt_dirname_formatter
