.. main file for lpedit documentation

Bayesian linear regression in R
====================================

Save the `model-of-the-mean` example as `linear-regression-example.rst`.  Open it and lets get started.

   1. Have a look at the linear regression formula.
      
      .. math::
         
         t_{n} = w_{0} + w_{1}x_{1}\\
               &= \sum^{M-1}_{j=1} w_{j} \mathbf{x}\\
               &= \mathbf{w}^{T} \mathbf{x}


   .. code-block:: r

      sink("example-sink.txt")
      cat("model{
          # priors
          for (i in1:nGroups){
              w0[i] ~ dnorm(0,0.001)
              w1[i] ~ dnorm(0,0.001)
          }  
      }
      ",fill=TRUE)
      sink()