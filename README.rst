**********
pytest-plt
**********

``pytest-plt`` provides fixtures for
quickly creating Matplotlib plots in your tests.

Create PDF plots in one line with the ``plt`` fixture.

.. code-block:: python

   def test_rectification(plt):
       values = list(range(-10, 10))
       rectified = [-v if v < 0 else 0 for v in values]
       assert all(v >= 0 for v in values)
       plt.plot(values)

.. image::

To use these fixtures, install with

.. code-block:: bash

   pip install pytest-plt

And pass the ``--plots`` option

.. code-block:: bash

   pytest --plots my_plots

If you do not pass the ``--plots`` option,
no Matplotlib commands will be executed,
speeding up test execution.

See the
`full documentation <https://www.nengo.ai/pytest-plt>`__
for more details and configuration options.
