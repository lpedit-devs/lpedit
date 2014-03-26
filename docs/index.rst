.. main file for lpedit documentation

lpEdit - towards reproducible research
=============================================

Reproducibility in research can be divided into experimental and analytic components. The aspects of data sharing, leaving an audit trail and documentation are essential to reproducible research, whether it is in the laboratory or on a computer. :doc:`lpEdit <lpEdit>` is a cross-platform application that enables a broad range of scientists to carry out the analytic component of their work in a reproducible manner---through the use of literate programming.

:doc:`lpEdit <lpEdit>` is a way to perform data analyses such that the code and prose are mixed to produce a final report that reads like an article or book. The extensive use of templates and documentation reduces the learning burden on researchers. In addition, an editor designed specifically for the task of literate programming minimizes the technical understanding necessary to incorporate aspects of good reproducible practices into daily research routines.

This project is community-based and to learn more visit the :doc:`Contributors` page.

Main Contents:
----------------

.. toctree::
   :maxdepth: 1

   lpEdit - an editor for literate programming <lpEdit>
   Bayesian short course <BayesianCourse>
   Contributors
   References
    
How to use these documents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It can be helpful to install locally these documents because there are so many examples.

   1. `install Git <http://git-scm.com/book/en/Getting-Started-Installing-Git>`_
   2. install the Python package `Sphinx <http://sphinx-doc.org>`_
   3. Clone the repository either through the GUI or by

      .. code-block:: bash
       
         ~$ git clone https://github.com/lpedit-devs/lpedit.git

   4. build the documents with either ``latex`` or ``html`` 

      .. code-block:: bash
         
         ~$ cd lpedit/docs
         ~$ python initDocs.py

The documents are now available in ``./_sphinx/_build``.  

To update to the latest version of the repository use:

   .. code-block:: bash

      ~$ git pull

Then rebuild the documents.

It is also possible to use the editor component of :doc:`lpEdit` to compile the documents.  In this case:

      .. code-block:: bash
         
         ~$ cd lpedit/docs
         ~$ lpedit -f index.html

The ``Build``, ``Compile`` and ``View``.
