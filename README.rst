**********
pytest-plt
**********

``pytest-plt`` provides fixtures for
quickly creating Matplotlib plots in your tests.

Create PDF plots in one line with the ``plt`` fixture.

.. code-block:: python

   def test_rectification(plt):
       values = list(range(-10, 11))
       rectified = [v if v > 0 else 0 for v in values]
       assert all(v >= 0 for v in rectified)
       plt.plot(values, label="Original")
       plt.plot(rectified, label="Rectified")
       plt.legend()

.. image:: https://i.imgur.com/2BFq2G2.png

To use these fixtures, install with

.. code-block:: bash

   pip install pytest-plt

And pass the ``--plots`` option

.. code-block:: bash

   pytest --plots

Usage
=====

The ``plt`` fixture allows you to create PDF plots with as little as one line.
It exposes the ``matplotlib.pyplot``
`interface <https://matplotlib.org/api/pyplot_summary.html>`_.

When running your tests,
pass the ``--plots`` option (with optional directory name)
to generate the plots
(in this case, we save them to the "my_plots" directory):

.. code-block:: bash

   pytest --plots my_plots

If no directory name is provided,
plots will be saved to the "plots" directory:

.. code-block:: bash

   pytest --plots

If you do not pass the ``--plots`` option,
no Matplotlib commands will be executed,
speeding up test execution.

Custom filenames and extensions
-------------------------------

``pytest-plt`` attempts to give each plot
a readable name without being too long.
Sometimes the default name is not good enough,
so ``plt`` allows you to change it using ``plt.saveas``:

.. code-block:: python

   def test_rectification(plt):
       values = list(range(-10, 11))
       rectified = [v if v > 0 else 0 for v in values]
       assert all(v >= 0 for v in rectified)
       plt.plot(values, label="Original")
       plt.plot(rectified, label="Rectified")
       plt.legend()
       plt.saveas = "test_rec.png"

The ``plt.saveas`` attribute contains the
filename that will appear in the plots directory.
You can modify this attribute within your test
to change the filename that will be used
to save the plot for a given test function.
In the above example, running pytest with
``pytest --plots my_plots`` will result in
a ``my_plots/test_rec.png`` file.

It should be noted that the file extension
in ``plt.saveas`` will be used when saving the plot.
That is, in the example above,
the resulting plot will be a true PNG file,
not a PDF with an incorrect ``.png`` extension.
You can use the following snippet to change
the file extension in a specific test
if the PDF format is unsuitable.

.. code-block:: python

   plt.saveas = "%s.png" % (plt.saveas[:-4],)

Moreover, using the extension ``.pickle`` will tell pytest-plt to pickle the
current figure object. The figure can then be inspected using pyplot's
interactive GUI after unpickling the file. You can achieve this with the
following code snippet.

.. code-block:: python

   import pickle
   import matplotlib.pyplot as plt
   pickle.load(open('path/to/my/plot/figure.pickle', 'rb'))
   plt.show()

Configuration
=============

The following configuration options exist.

plt_filename_drop
-----------------

``plt_filename_drop`` accepts a list of regular expressions
for parts of the filename to drop.

By default, plot filenames contain the full ``nodeid``
for the test in question,
with directory separators (``/``) replaced with dots (``.``).
If all tests reside in the same project directory,
that name will appear at the start of all plot filenames,
making them unnecessarily long.

In this case, we use the carat ``^`` to ensure that
our regex matches the start of the filename only,
and we remove the trailing dot as well (``\.``):

.. code-block:: ini

   plt_filename_drop =
       ^project\.

If your tests always reside in a directory with a particular name
(e.g. "tests"),
you can safely remove this name wherever it occurs.
In this case, we do not use the carat to allow the regex to match anywhere
in the filename.
Be careful, as this will match any directory
that ends with "tests" (e.g. "other_tests"),
and will remove the ends of these directory names.

.. code-block:: ini

   plt_filename_drop =
       ^project\.
       tests\.

When using ``plt_filename_drop``, take care to avoid collisions
(situations where plots from two different tests
will end up with the same name).
In this case, the plots of later tests
will override those of earlier tests with the same name.

plt_dirname
-----------

``plt_dirname`` changes the default directory name for output plots.

The default ``plt_dirname`` is ``"plots"``.
To change it to ``"test_plots"``, for example, add the following
to your ``pytest.ini``.

.. code-block:: ini

   plt_dirname = test_plots

A directory provided at the command line with the ``--plots`` flag
takes priority over ``plt_dirname``.

See the full
`documentation <https://www.nengo.ai/pytest-plt>`__
for more details and configuration options.
