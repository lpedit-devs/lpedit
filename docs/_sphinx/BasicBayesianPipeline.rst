.. reproducible research tutorial file, created by ARichards

About the basic analysis pipeline
===================================

The basic procedure for fitting a model.

  1. Select a Model
  2. Write a BUGS model to a text file with your :doc:`Editor`
  3. Create a script with basic R commands like loading data
  4. Prepare the inputs for the JAGS
  5. Run the model
  6. Make plots and assess convergence
  7. Summarize the posterior
  
Some of the key words that we will become familiar with are: **posterior**, **prior**, **likelihood**, **MCMC**, **initial values**, **updates** and **convergence**

What is a model?
-----------------------------

*Estimate the mean of a normal population from a sample of measurements*


.. rubric:: simple-mean

.. code-block:: r 

  somedata = rnorm(10)
  print(somedata)
  print(mean(somedata))


.. code-block:: none 

  [1] "..."
  [1]  0.5034817 -1.2082534 -0.8914252  0.6738340  1.5205681  1.4631499
  [7]  1.2189704 -0.6773669 -1.3231847 -0.8199908
  [1] 0.04597831
   


Models imply assumptions.  Not all models are appropriate even one as simple as the model of the mean-- think of skewed or correlated data.  Summary statistics are models.  Standard error, standard deviation, coefficient of variation etc.

If we just want to fit a common mean to :math:`y`.

   :math:`\textrm{mass}_{i} = \mu + \epsilon_{i}`

This is the same as fitting a linear model with intercept only.   
   

.. rubric:: lm-simple

.. code-block:: r 

  print(lm(somedata ~ 1))


.. code-block:: none 

  [1] "..."
  
  Call:
  lm(formula = somedata ~ 1)
  
  Coefficients:
  (Intercept)  
      0.04598  
  
   


Open up a editor and follow along
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generally each analysis should have its own directory-- it make sense if we want to bundle the methods, data and report.  Start from an empty `*.Rnw` template in a directory called `model-of-the-mean`.

   1.  :download:`linreg-data.csv <../linreg-data.csv>`

      .. literalinclude:: ../linreg-data.csv

   2. Load the data
      
      .. code-block:: r
      
         > data <- read.csv("../linreg-data.csv",header=TRUE,sep=',')
         > attach(data)
         > print(names(data))

         
   3. Plot the data     
         
      .. code-block:: r
         
         pdf("linreg-data.pdf",height=6,width=6)
         hist(y,col='grey',main="distribution of y")
         dev.off()     
         
      .. code-block:: tex 
        
         \begin{figure}
         \begin{center}
         \includegraphics[ext=.pdf,scale = 0.9]{"linreg-data"}
         \end{center}
         \caption{This is the figure caption}
         \end{figure}

   4. Add an example of a formula.  After all it is :math:`\textrm{\LaTeX}`.

      .. math::
  
         t_{n} &= w_{0} + w_{1}x_{1}\\
               &= \sum^{M-1}_{j=1} w_{j} \mathbf{x}\\
               &= \mathbf{w}^{T} \mathbf{x}

      Here are the commands you will need:
         * ``\usepackage{amsmath}``
         * subscript ``x_{i}`` superscript ``x^{i}`` 
         * ``\sum^{}_{}``
         * ``\mathbf{}``

         * .. code-block:: tex

              \begin{align}
                 x^{2}      &= x \times x \\
                 e^{\ln(2)} &= 2
              \end{align}

         .. note:: what if you use ``align*``?  or if you put the ``&`` at the beginning of each line?
      
   6. Show and example of how to save data to file.  The following code will help you figure it out

      .. code-block:: r
         
         > a <- rnorm(10)
         > b <- rnorm(10)
         > ab <- data.frame(a,b)
         > dump("ab",file="ab.R")
         > rm(ab)
         > source(file="ab.R")
         > ab

   7. Edit/create your model, inits and command files

      First try this with the provided files.  Then if you wish the model and command files can be written to file from your sweave documents using the ``cat`` and ``sink`` commands. The inits file can be written with ``dump``. 

      .. code-block:: r

         sink("model.txt")
         cat("model{
             # priors
             population.mean ~ dunif(0,5000)       # normal parameterized by precision
	     precision <- 1 / population.variance  # Precision = 1 / variance
             population.variance <- population.sd * population.sd
             population.sd ~ dunif(0,100)
             
             # likelihood
             for(i in 1:N){
               mass[i] ~ dnorm(population.mean, precision)
             }
	    }   
         ",fill=TRUE)
         sink()
         
      ..code-block:: r
      
         n <- length(y)
         jagsData <- list(y=y,n=n)

         #Inits function
         inits <- function()
           list(population.mean = rnorm(1,10), population.sd = runif(1,1,30))
         
         params <- c("population.mean", "population.sd", "population.variance")
         
         # MCMC
         
         nc <- 3          # number of chains
         
   8. run it (if not part of script)

      .. code-block:: bash

         ~$ jags line-reg-simple.cmd
         
      or
      
      .. code-block:: r
      
         > system("jags line-reg-simple.cmd")