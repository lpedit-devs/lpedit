.. main file for lpedit documentation

Bayesian linear regression in R
====================================

.. note:: A prior distribution does not necessarily imply a temporal priority, instead, it simply represents a specific assumption about a model parameter. Bayes rule tells us how to combine such an assumption about a parameter with our current observations into a logical, quantitative conclusion. The latter is represented by the posterior distribution of the parameter (see [Kery10]_, page 17).

A prior may be uninformative for a data set, but upon transformation with say ``log`` the assumptions about a prior may no longer hold.

A bit more on the model of the mean
---------------------------------------

.. literalinclude:: snakes.csv

<<read-data>>=
## read in the data
data <- read.csv("./bayesian-course/snakes.csv",header=TRUE,sep=',')
attach(data)

## use factors where values are not quantitative
pop <- as.factor(pop)
region <- as.factor(region)
hab <- as.factor(hab)
@

In the previous example we just fit a common mean to the ``mass`` of all six snakes.  In R again this is written as:

<<show-lm>>=
print(lm(mass~1))
@

This implies a single covariate with a single value for each snake.  This means that the ``mass`` of individual snake :math:`i` is represented as an overall mean plus some deviation.

   .. math::
   
      \textrm{mass}_{i} = \mu + \epsilon_{i}

The individual deviation is called :math:`\epsilon_{i}`.  This is also called the **residual** for snake :math:`i`.  We are going to assume a distribution for these residuals. 

   .. math::
   
     \epsilon_{i} \sim \mathcal{N}(0,\sigma^{2})

Behind the scenes when we run ``lm`` R is creating something called a **design matrix**.  It is a very important function that helps us understand what is going on.

<<show-design-matrix>>=
print(model.matrix(mass ~ 1))
@


t-test
---------------

If we are interested in the effect of a single binary variable like ``region`` on ``mass`` we can use a t-test.

<<lm-ttest>>=
print(summary(lm(mass~region)))
@

This can be written as:

   .. math::
   
      \textrm{mass}_{i} = w_{0} + w_{1} \textrm{ region}_{i} + \epsilon_{i}
      
   
So under this model the ``mass`` of snake :math:`i` is made up of three components.  We use the same Gaussian (normal) distribution assumption about residuals.

   .. math::
   
      \textrm{mass}_{i} = \textrm{N}(w_{0} + w_{1} \textrm{ region}_{i} + \epsilon_{i}, \sigma^{2})

If we assume :math:`\epsilon_{i} \sim \mathcal{N}(0,\sigma^{2})` then we should test for normality of the individual residuals when using a t-test.

<<t-test-design-matrix-effect>>=
model.matrix(~region)
@

The indicator variable ``region2`` contains a 1 for the snakes that are in region 2.  Region 1 becomes a base level and we see the **effect** of region 2 compared to region 1.  The value of the intercept is then the mean ``mass`` of snakes in region 1.  This setup is known as the **effects parameterization**.  An equivalent way to look at differences in regions with respect to ``mass`` is to reparameterize the model as a **means parameterization**.

<<t-test-design-matrix-means>>=
print(model.matrix(~region-1))
print(lm(mass~region-1))
@

The effects parameterization lets us test for differences for means between the two regions and the means parameterization lets us report the expected mass of snakes for each region.  They are equivalent models.

Simple Linear Regression
----------------------------

To examine the response between a continuous response variable ``mass`` and a continuous explanatory variable ``svl``.  We use simple linear regression. 

   .. math::
   
      \textrm{mass}_{i} = w_{0} + w_{1} \textrm{ svl}_{i} + \epsilon_{i}

      
The difference between this and a t-test is in the contents of the explanatory variable.  Here is the design matrix.
      
<<linreg-design-matrix>>=
print(model.matrix(~svl))
@     

Download: :download:`LinearRegression.rnw`

.. literalinclude:: LinearRegression.rnw
   :language: latex

Which parameterization to use   
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   

<<linear-reg-effects-in-R>>=
print(lm(mass~svl))
@

The intercept has little meaning as it says that a snake of length 0 weight -5.6 units.  We can give the model a more relevant meaning by transforming ``svl``

.. math::

   \textrm{svl} = svl - mean(svl)
     
<<linear-reg-adjusted-intercept-in-R>>=
msvl <- svl - mean(svl)
print(lm(mass~msvl))
@

This will cause the intercept to become the expected mass of a snake at the average of the observed size distribution.

.. note:: Try changing you code to reflect this.  Hint: ``mean`` is a function in BUGS.
