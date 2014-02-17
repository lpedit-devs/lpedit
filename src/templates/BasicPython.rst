.. A basic template for Python using reST

==========================
A Basic Python Example
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
import numpy as np
N = 4
M = 5
mat = np.random.normal(0,1,(N,M))
print(mat)
@ 

Useful links
==========================

* The `official Python website <http://www.python.org>`_
* A `restructuredtext quick ref <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
