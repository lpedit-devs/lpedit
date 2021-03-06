.. reproducible research tutorial file, created by ARichards

Gibbs samplers
==============

What is a Gibbs sampler
-------------------------------

`Gibbs sampling <http://en.wikipedia.org/wiki/Gibbs_sampling>`_ is a `Markov Chain Monte Carlo algorithm <http://en.wikipedia.org/wiki/Markov_chain_Monte_Carlo>`_ for obtaining samples from a posterior distribution.  We can think of the Gibbs sampler in simple terms as the tool to carry out the `mathematical optimization <http://en.wikipedia.org/wiki/Mathematical_optimization>`_ step for our model.  Most biologists do not understand the algorithms behind the ``glm`` function in R so by that logic it is not necessary to understand everything about MCMC.  That being said our MCMC samplers will be providing a chain of samples that we need to be familiar with.  As you get better interfacing with your MCMC sampler it is in your best interest to dig in and learn a bit more.          

BUGS means Bayesian Inference Under Gibbs Sampling.  The BUGs language was developed in the 1990's [Gilks94]_. A place for more information is the `BUGS project <http://www.mrc-bsu.cam.ac.uk/bugs/>`_.  Much of the work on BUGS has been for a variant specifically designed for windows called WinBUGS [Lunn09]_.

Why why why??
^^^^^^^^^^^^^^^^^^^^

The BUGS language is our key to the Bayesian world.  It allows us to specify almost arbitrarily complex statistical models using a fairly simple model definition language.  We can describe `deterministic <http://en.wikipedia.org/wiki/Deterministic_system>`_ and `stochastic <http://en.wikipedia.org/wiki/Stochastic>`_ variables for all **observed** and **unobserved** variables.  We specify the full model including `priors <http://en.wikipedia.org/wiki/Prior_probability>`_, provide the data, and the sampler does the rest.  That is it collects some number of samples from the `joint probability distribution <http://en.wikipedia.org/wiki/Joint_probability_distribution>`_.  

Installation
--------------------

For the purposes of the class all examples will be using JAGS.  JAGS works on all platforms, it is well maintained and there are R packages to simplify your life.  WinBUGS and OpenBUGS may work for you system, but it is up to you to learn how to get things going.  They are all for practical purposes basically the same. 

On windows
^^^^^^^^^^^^^^^

You have the choice.  There are several Gibbs samplers that work well on windows.

   * `WinBUGS <http://www.mrc-bsu.cam.ac.uk/bugs/winbugs/contents.shtml>`_
   * `OpenBUGS <http://www.openbugs.info/w/FrontPage>`_
   * `JAGS <http://mcmc-jags.sourceforge.net>`_

I am not actively tesing on window so here are a couple of websites that might help you get started with BUGS going on your machine.  It is apparently different if you have a 32 or 64 bit machine.  The second link has quite a lot of details on installation.  The examples in this website are tested using JAGS.

   * `http://www.stat.cmu.edu/~brian/463/install-winbugs.html <http://www.stat.cmu.edu/~brian/463/install-winbugs.html>`_ 
   * `http://faculty.washington.edu/jmiyamot/p548/installing.bugs.jags.pdf <http://faculty.washington.edu/jmiyamot/p548/installing.bugs.jags.pdf>`_

OSX
^^^^^^

To install `JAGS <http://mcmc-jags.sourceforge.net>`_ click on the `sourceforge link <http://sourceforge.net/projects/mcmc-jags/files/latest/download?source=files>`_
   
On GNU/Linux
^^^^^^^^^^^^^^^
  
   .. code-block:: bash

      ~$ sudo apt-get install jags
      
    
For non-debian based distros use the `sourceforge page <http://mcmc-jags.sourceforge.net>`_ for more information.

R2jags
^^^^^^^^^^^^^^^^^

JAGS is a standalone program meaning that it can be run alone.  However, it is common that people use packages in R to interface with JAGS.  This is because we read, manipulate and plot data in R so it is convenient if we can input directly from R.  Also, JAGS, like all MCMC samplers tends to produce a lot of output so a package with that reads these data is useful.

Open an R terminal and type the following.

  .. code-block:: r

     > install.packages("rjags", dependencies=TRUE)
     > install.packages("R2jags", dependencies=TRUE)

To check that it worked go into R and type

  .. code-block:: r
  
    > library(rjags)
     
Resources
^^^^^^^^^^^^^

   * `JAGS <http://mcmc-jags.sourceforge.net>`_ - sourceforge website
   * `WinBUGS <http://www.mrc-bsu.cam.ac.uk/bugs/winbugs/contents.shtml>`_ - official winbugs site
   * `BUGS project <http://www.mrc-bsu.cam.ac.uk/bugs/>`_
   * `Andrew Gelman's page <http://andrewgelman.com/2009/02/08/our_new_r_packa/>`_