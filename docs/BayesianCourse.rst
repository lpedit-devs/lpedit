.. Reproducible Research About.rst

Bayesian short course
=======================

Welcome to a short course in Bayesian statistics.  This course is being taught in March 2014 at Station d'Ecologie Exp\ :math:`\textrm{\'{e}}`\ rimentale du CNRS :math:`\textrm{\`a}` `Moulis <http://www.ecoex-moulis.cnrs.fr>`_.  The goal of the course is to use a :doc:`literate programming <LiterateProgramming>` style of analysis to carry out statistical tests commonly encountered in the biological sciences.  A major reason for using this style is that if you do it well once then you do not have to re-learn it again.  

All examples from this course can be reproduced easily.  Of course this course is also about Bayesian statistics and the scope is fairly limited, but focused on doing a few things well.  Interested participants will be pointed to resources along the way to further their understanding of the different subjects.

Since the majority of the people taking this course are ecologists, much of this website is borrowed from Marc Kery's book *Introduction to WinBUGS for Ecologist* [Kery10]_.  Here is the `book's website <http://www.mbr-pwrc.usgs.gov/software/kerybook/>`_ where there is also another more advanced book called *Bayesian Population Analysis using WinBUGS*.  It is probably the most accessible piece of Bayesian literature that I have ever read and the examples are quite useful.

What you will Need
^^^^^^^^^^^^^^^^^^^^^^

   1. :doc:`Latex` - a working version of :math:`\textrm{\LaTeX}` installed
   2. :doc:`R` - a current version of the statistical language R
   3. :doc:`Editor` - an editor that compiles :doc:`Sweave`
   4. :doc:`BUGS` - Though several software are available we recommend `JAGS <http://mcmc-jags.sourceforge.net>`_
   5. Install `rjags` and `R2jags` - See the :doc:`BUGS` page for more info
   
      Open an R terminal and type the following.

      .. code-block:: r

         > install.packages("rjags", dependencies=TRUE)
         > install.packages("R2jags", dependencies=TRUE)
 
That is only 5 things, all of which are free.  In order to run the examples here you will need all of them working.
 
.. note::

   As an editor it will be easiest to use `RStudio <https://www.rstudio.com>`_.  However, :doc:`lpEdit` may be used for those looking to use languages other than R.  It is also possible for those who are inclined to avoid graphical interfaces entirely.  Something like `Emacs <http://www.gnu.org/software/emacs/>`_ or another such editor could be used so that the examples are run from the command line.

Course Contents
--------------------

.. toctree::
   :maxdepth: 2

   BayesianDay1
   BayesianDay2
   
   
Other helpful materials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * `The command line crash course <http://cli.learncodethehardway.org/book>`_ - a book
  * `Bayesian statistics made (as) simple (as possible) <http://www.youtube.com/watch?v=bobeo5kFz1g>`_ - a youtube video