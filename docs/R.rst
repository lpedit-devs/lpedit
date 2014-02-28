.. reproducible research tutorial file, created by ARichards


R
=

The `R <http://www.r-project.org>`_ computing environment is the *Lingua franca* for the statistics community.  R is already adapted to
reproducible research, most commonly through the use of :doc:`Sweave` and the R community is actively addressing the problem of
`reprodubibility <http://en.wikipedia.org/wiki/Reproducibility>`_ as evidenced by the number of `reproducible research packages in CRAN <http://www.cran.r-project.org/web/views/ReproducibleResearch.html>`_.

Installation
-----------------

If you do not already have `R <http://www.r-project.org>`_ installed on your machine then: 

GNU/Linux
^^^^^^^^^

Under Debian-based GNU/Linux distros:

    .. code-block:: none

        ~$ sudo apt-get install r-base-dev

Under Fedora/Red Hat distros:

    .. code-block:: none

        ~$ sudo yum install R


Mac OS X
^^^^^^^^

Visit the `official installation page for OS X <http://cran.r-project.org/bin/macosx>`_.

Windows
^^^^^^^

Visit the `official installation page for Windows <http://cran.r-project.org/bin/windows/base>`_. 
Also there is a `Windows install FAQ <http://cran.r-project.org/bin/windows/rw-FAQ.html>`_ page.

Running R
------------

<<calculator>>=
ans <- 2 + 5
print(ans)
@

R can be thought of as a calculator that does a great many things.  It is important to understand that R can be run **interactively** or as a **script**.

Useful links
^^^^^^^^^^^^^^^

* The `official R website <http://www.r-project.org>`_
* The `Use R conference <http://biostat.mc.vanderbilt.edu/wiki/Main/UseR-2012>`_
