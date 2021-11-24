***************
Release History
***************

.. Changelog entries should follow this format:

   version (release date)
   ======================

   **section**

   - One-line description of change (link to Github issue/PR)

.. Changes should be organized in one of several sections:

   - Added
   - Changed
   - Deprecated
   - Removed
   - Fixed

1.1.1 (unreleased)
==================

**Changed**

- Python 3.5, which is past its end of life, is no longer supported. (`#26`_)

**Fixed**

- Config options are now properly added to Pytest, eliminating a warning
  that was raised if a config option was set. (`#26`_)

.. _#26: https://github.com/nengo/pytest-plt/pull/26

1.1.0 (August 17, 2020)
=======================

**Added**

- Added the ability to save plots as pickle files using the
  ``.pkl`` or ``.pickle`` extensions with ``plt.saveas``. (`#23`_)

.. _#23: https://github.com/nengo/pytest-plt/pull/23

1.0.1 (October 28, 2019)
========================

**Fixed**

- We now use Windows-compatible plot filenames by default.
  Colons in plot filenames are replaced with hyphens.
  Filenames specified through ``plt.saveas`` are not modified.
  (`#17`_, `#21`_)

.. _#17: https://github.com/nengo/pytest-plt/issues/17
.. _#21: https://github.com/nengo/pytest-plt/pull/21

1.0.0 (August 9, 2019)
======================

Initial release of ``pytest-plt``!
Thanks to all of the contributors for making this possible!
