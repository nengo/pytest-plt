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

1.0.2 (unreleased)
==================

**Added**

- Added the ability to save plots as pickle files using the
  ``.pickle`` extension with ``plt.saveas``. (`#23`_)

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
