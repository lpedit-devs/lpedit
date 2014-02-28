.. sweave


Sweave
======

What is Sweave?
-----------------------

`Sweave <http://www.statistik.lmu.de/~leisch/Sweave>`_ is a tool that enables users to embed `R <http://www.r-project.org>`_ code into
reports.  It is a powerful tool for :doc:`LiterateProgramming` that is the focus of this web-resource, however there are
:ref:`sweave-alternatives` for the R statistical environment.

Installing Sweave
-------------------

The Sweave package is part of `R <http://www.r-project.org>`_.  If you
do not already have R installed on your machine then visit the :doc:`R
page<R>`.  In addition to the R computing envrionment, it is also
required that you have :math:`\textrm{\LaTeX}` installed.  If
:math:`\textrm{\LaTeX}` is not yet available on your system or if you
wish to learn more visit the :doc:`LaTeX information page <Latex>`.
Finally, before we get into the essentials of Sweave you will have be
familiar with and have handy your :doc:`programming editor <Editor>`.

A simple example
--------------------

Sometimes in programming it is easiest for learning to jump right in
with and example then to go back through that exampled and try to
break it apart.  Here is a fairly simple example that will run a
Fisher's exact test.

Open an :doc:`editor <Editor>` and save the following as
FishersExactTest.Rnw otherwise use the download link below.


.. literalinclude:: /../../lpedit/examples/FishersExactTest.Rnw
   :language: latex



Now visit the following to get more familar with the example that you just ran.

.. toctree::
   :maxdepth: 1

   SweaveExampleWalkthrough
		  
Running the code (from a command prompt)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sweave files look a lot like  :math:`\textrm{\LaTeX}` files.  Running the next few commands will produce your Sweave report.  **R CMD Sweave** tells R to use Sweave to evaluate the file and produces a .tex file.  The next command **pdflatex** uses :math:`\textrm{\LaTeX}` to produce a pdf report and the final line is a shortcut to view the report.  For a more detailed explination of this example visit the :doc:`SweaveExampleWalkthrough`. In order to run these commands you must first navigate to the directory containing FishersExactTest.Rnw.  It is also nice to let each Sweave report reside in its own directory because both Sweave and :math:`\textrm{\LaTeX}` produce numerous extra files during compilation. 

* GNU/Linux
    .. code-block:: none

        ~$ R CMD Sweave FishersExactTest.Rnw 
        ~$ pdflatex FishersExactTest.tex
        ~$ evince FishersExactTest.pdf
* Max OS X
    .. code-block:: none

        ~$ R CMD Sweave FishersExactTest.Rnw 
        ~$ pdflatex FishersExactTest.tex
        ~$ open FishersExactTest.pdf
* Windows
    .. code-block:: none

        ~$ R CMD Sweave FishersExactTest.Rnw 
        ~$ pdflatex FishersExactTest.tex
        ~$ adobereader FishersExactTest.pdf

Alternatively, we have created a tool (:doc:`lpEdit`) that uses Sweave
syntax, but does not require the user to enter the command line.  RStudio will also run Sweave documents.

.. _sweave-alternatives:

Alternatives to Sweave
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* `decumar <https://github.com/hadley/decumar>`_
* `knitr <http://yihui.name/knitr>`_
