**********
lpedit
**********

:Version: 0.5
:Authors: Adam Richards
:Web site: https://github.com/lpedit-devs/lpedit
:Documentation: http://lpedit-devs.github.io/lpedit/
:Copyright: This document has been placed in the public domain.
:License: lpedit is released under the 3-clause BSD License


About
========

lpEdit is an API for literate programming in R and Python through the use of LaTeX and reStructuredText.  This tool is essentially a report creation utility that helps make statistical analyses more reproducible. 

See the documentation for instructions on installation.

lpedit is undergoing some changes

  * moved to a less restrictive BSD license
  * freezing development of the GUI editor


Installation
===============

For more details visit the documentation:

  *  http://ajrichards.github.io/lpedit

The easiest way to install and maintain ``lpedit`` is to use `pip <https://pypi.python.org/pypi/pip>`_

  .. code-block:: bash

      ~$ pip install lpedit

  .. code-block:: bash

      ~$ pip install lpedit --upgrade

The source is also available on GitHub and may be installed using:

  .. code-block:: bash

      ~$ python setup.py install


Getting started
===================

To create a document this example illustrates the generalized syntax:

  .. code-block:: python

     from lpedit import NoGuiAnalysis
     fileName = 'report-name.nw'
     language = 'python'
     nga = NoGuiAnalysis()
     nga.load_file(fileName,fileLang=language)
     nga.build(fileName)
     nga.compile_pdf()


Using lpedit in a publication or technical report?
====================================================

Read the `proceedings PDF <http://conference.scipy.org/proceedings/scipy2013/pdfs/richards.pdf>`_ or use the following BIBTEX entry.

.. code-block:: none

   @InProceedings{richards-proc-scipy-2013,
      Title              = { lpEdit: an editor to facilitate reproducible analysis via literate programming },
      Author             = {Adam J Richards and Andrzej S. Kosinski and Camille Bonneaud and Delphine Legrand and Kouros Owzar},
      Book title         = { Proceedings of the 12th Python in Science Conference },
      Year               = { 2013 },
      Editor             = { St\'efan van der Walt and Jarrod Millman and Katy Huff },
      Pages              = { 85 - 89 }
   }
	     
