.. A basic template for R using reST

==========================
A Basic R example
==========================

Section Title
==========================

.. This is a comment 
   Comment may also be multiline

We show in this example how to create a matrix of random numbers.
The matrix has :math:`N` rows and :math:`M` columns.

A subsection
^^^^^^^^^^^^^^^^^^^^^^^^^^

<<label=chunk1>>=
N <- 4  
M <- 5  
mat <- matrix(rnorm(M*N), N) 
print(mat)
@

Useful links
==========================

* The `official R website <http://www.r-project.org>`_
* A `restructuredtext quick ref <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
