.. reproducible research tutorial file, created by ARichards
.. INCLUDE example-latex.pdf


LaTeX
=====

:math:`\textrm{\LaTeX}` is a typesetting language.  Reports, articles, journal articles, dissertations, presentations and books are commonly written in :math:`\textrm{\LaTeX}`.  As a scientist :math:`\textrm{\LaTeX}` is the standard for carrying out research in a reproducible way.  Word processors tend to use binary format, which inhibit the use of technologies that help with :doc:`auditing <AuditTrail>`.  Moreover, word processors have compatibility issues between versions and between comparable programs.  Most, importantly, :math:`\textrm{\LaTeX}` is freely available and produces high quality attractive documents.

Installation
-------------

.. toctree::
    :maxdepth: 1

    LatexInstallWindows
    LatexInstallOSX
    LatexInstallLinux

Example Document
-----------------

An example document written in :math:`\textrm{\LaTeX}`.

    .. code-block:: tex

        \documentclass[12pt]{article}
        \usepackage{amsmath} 
        \title{A sample document}
        \author{Author Name}
        \date{\today}

        \begin{document}
        \maketitle
  
        This is where the text goes.  Mathematical
        formulae, like $e=mc^{2}$ can easily be included.
  
        \end{document}

:math:`\textrm{\LaTeX}` documents need to be compiled into PDF, HTML,
Postscript or another format that the user specifies.  Editors (see
editor list below) can compile these documents at the click of a
button.  Otherwise, you can navigate to the folder where a file is
saved and use:

    .. code-block:: bash
    
        $ pdflatex name-of-latex-document.tex

To view the output of the above document as a PDF.

    * :download:`example-latex.pdf`
    

LaTeX Editors
^^^^^^^^^^^^^^^

    * `TeXnicCenter <http://www.texniccenter.org>`_
    * `Texmaker <http://www.xm1math.net/texmaker>`_
    * `Kile <http://kile.sourceforge.net>`_
    * `Wiki's comparison of TeX editors <http://en.wikipedia.org/wiki/Comparison_of_TeX_editors>`_

Resources
^^^^^^^^^^^^^^

    * `Main LaTeX page <http://www.latex-project.org/>`_
    * `Help with LaTeX <http://www.latex-project.org/help.html>`_
    * `Getting started with LaTeX <http://www.maths.tcd.ie/~dwilkins/LaTeXPrimer>`_
    * `Formula help <http://fr.wikipedia.org/wiki/Aide:Formules_TeX>`_
    * `A reference card <http://www.math.brown.edu/~jhs/ReferenceCards/LaTeXRefCard.v2.0.pdf>`_