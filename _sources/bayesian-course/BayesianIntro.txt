.. main file for lpedit documentation

Brief introduction to Bayesian statistics
=============================================

This is mostly borrowed from Marc Kery's book [Kery10]_.

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

Bayesian inference works by combining information about parameters :math:`\theta` contained in the observed data :math:`x` as quantified in the likelihood function :math:`p(x|\theta)`.  Classical statistics works by making inference about a single point, while Bayesian inference works on the whole distribution.  Parameters through the Bayesian lens are treated as random variables described by distributions.

Lets try with an example.

**Predictive value positive** - Prob. person has disease given the test was positive.
   :math:`PV^{+} = P (D^{+} |T^{+})`

**Predicitve value negative** - Prob. person does not have diease given test was negative 
   :math:`PV^{−} = P (D^{−} |T^{−} )`    

**Sensitivity** - Prob. that test positive given person has disease 
   :math:`P (T^{+} |D^{+})`
   
**Specificity** - Prob. that test negative given person does not have disease 
   :math:`P (T^{−} |D^{−})`

**Prevalance** - :math:`d = P(D^{+})`
   
Note that: :math:`P (T + |D − ) = 1 - \textrm{specificity}`

Lets say we wanted to know :math:`PV^{+}`.
   
   .. math::
      :nowrap:

      \begin{eqnarray}
      P (D^{+} |T^{+}) &=& \frac{P(T^{+}|D^{+}) P(D^{+})}{P(D^{+})P(T^{+}|D{+})+P(D^{−})P(T^{+}|D^{−})} \\
                       &=& \frac{d∗\textrm{sensitivity}}{d∗\textrm{sensitivity}+(1−d)∗(1−\textrm{specificity})} 
      \end{eqnarray}
      
So if we were given

Sensitivity = 0.84, specificity = 0.77, prevalence = 0.20

Then

   .. math::
    
      PV^{+} = \frac{(0.2)(0.84)}{(0.2)(0.84)+(0.8)(0.23)}  = 0.48 \\
      PV^{-} = \frac{(0.8)(0.77)}{(0.8)(0.77)+(0.2)(0.16)}  = 0.95

      
      
Resources
^^^^^^^^^^^^^^^^^^^^

  * `Decent blog about Bayesian inference in R <http://blogs.uoregon.edu/bayesclub/tag/r2jags>`_
  * `JAGS tutorial <http://jkarreth.myweb.uga.edu/bayes/jags.tutorial.pdf>`_ - a pdf
