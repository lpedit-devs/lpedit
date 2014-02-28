.. literate programming


Literate programming
====================

The idea of 'literate programming' was invented by `Donald Knuth <http://www-cs-faculty.stanford.edu/~knuth>`_.  The concept is quite simple---the decriptions that accompany code should be informative and progress from beginning to end with logical and clearly written text. This is in contrast from the more conventional style of terse commenting used in software development.  Another important part of literate programming is that the code embedded within the text should be easily run by the reader, which necessitates the use of working examples.

Literate programming does not have to be restricted to developers.  A driving force behind the creation of :doc:`lpEdit` was so that
researchers of many backgrounds could incorportate literate programming into their scientific lives.

This is a document.  And the goal is to be able to embed code that is run when the document is created.  For example if I cannot remember how do write a recursive function.


.. rubric:: for-example

.. code-block:: python 

  def factorial(n):
      if n == 0:
          return 1
      else:
          return n * factorial(n - 1)
  print(factorial(10))


.. code-block:: none 

  ...
  3628800
   


We can be sure the function works because an error would not allow the document to be made.

Notable Software 
----------------------


* `Python <http://www.python.org>`_ object-oriented scripting language
* `Pweave <http://mpastell.com/2010/03/03/pweave-sweave-for-python>`_ Sweave package for Python
* `PyLit  <http://pylit.berlios.de>`_ package for literate programming in Python using reStructuredText
* `pyreport <http://gael-varoquaux.info/computers/pyreport>`_ Another package for literate programming in Python
* `R <http://www.r-project.org>`_ software for statistical computing
* `Sweave <http://www.statistik.lmu.de/~leisch/Sweave>`_ the Sweave package
* `Ruby <http://www.ruby-lang.org/en>`_ another object-oriented language 
* `Rubyweb <http://www.cse.dmu.ac.uk/~hgs/ruby/rubyweb/index.html>`_ A web-oriented literate programming system
* `Sphinx <http://sphinx.pocoo.org>`_ works with Python, C/C++, Ruby, JS and others

Additional Resources
-----------------------

* `literateprogramming.com <http://www.literateprogramming.com>`_
