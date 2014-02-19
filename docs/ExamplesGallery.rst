.. reproducible research tutorial file, created by ARichards

===================
Gallery of examples
===================

The software editor :doc:`lpEdit` focuses on two languages: :doc:`R`
and `Python <http://python.org>`_.  Reports generated using :doc:`R`
make use of :doc:`Sweave` when combining :doc:`R` code and prose. For
the `Python <http://python.org>`_ programming language :doc:`lpEdit`
uses `Sphinx <http://sphinx-doc.org>`_ and reStructuredText to combine
code and prose.

The majority of examples in this gallery are written for Python and R,
because the code may be run at the same time the report is created,
which provides for a highly reproducible framework.  Additional
languages like Ruby and C/C++ may be used via Sphinx, however there
is no simple way to run the code at the time of report generation.

Examples by category
____________________

* :ref:`Python-examples`
* :ref:`R-examples`

.. _python-examples:

Python examples
_______________
Either a reST (rst) or noweb (nw) document that contains embedded Python code. 
These documents can be run using :doc:`lpEdit`.

.. toctree::
   :maxdepth: 1

   examples-gallery/BasicPythonInLatex
   examples-gallery/PlotsPythonInLatex
   examples-gallery/PermutationTest
   examples-gallery/bayes-linreg
   examples-gallery/BeamerPresentation

.. _R-examples:

R examples
__________

These are the :doc:`R` examples that use :doc:`Sweave`.  These
documents can be run using either normal :doc:`Sweave` syntax or via :doc:`lpEdit`.

.. toctree::
   :maxdepth: 1

   examples-gallery/BasicSweave
   examples-gallery/PlotsInSweave





