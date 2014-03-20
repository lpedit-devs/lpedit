.. main file for lpedit documentation

Brief introduction to Bayesian statistics
=============================================

This is mostly borrowed from Marc Kery's book.

Advantages of the Bayesian approach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   * Numerical Tractability -- Classical statistical methods do not always work
   * Absence of Asymptotics -- What is a large number?
   * Ease of Error Propagation -- Dealing in uncertainty
   * Formal framework for combining information -- prior
   * Intuitive appeal -- intrepretation is more intuitive
   * Coherence and intellectual beauty

Why isn't everyone a Bayesian
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   * Perceived subjectivity
   * Bayesian methods are amazing for complex models, but are they necessary for simpler ones?
   * Many of the books out there are difficult reads
   * Requires a deeper understanding of your model to implement
   * Implementation...
   * Easy to grasp examples...

Bayes Theorem
^^^^^^^^^^^^^^^^^^^^^

:math:`P(A|B) = \frac{P(B|A)P(A)}{P(B)}`    

:math:`P(\theta|x) = \frac{P(x|\theta)P(\theta)}{P(x)}`    

The **posterior** is proportional to the **likelihood** times the **prior** distribution

Bayesian inference works by combining information about parameter :math:`\theta` contained in the observed data :math:`x` as quantified in the likelihood function :math:`p(x|\theta)`.  Classical statistics works by making inference about a single point, while Bayesian inference works on the whole distribution.  Parameters through the Bayesian lens are treated as random variables described by distributions. 