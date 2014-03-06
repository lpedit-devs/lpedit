.. main file for lpedit documentation

Bayesian short course - day 1
=============================================

Day 1 is all about promoting good analysis habits.  We should be able to look back a year from now at this website or at the files you create to fit your own work and simply be able to understand and use them.

<<can-we-reproduce-our-own-analyses?>>=
def fib(n):
    a,b = 0,1
    while a < n:
        print("%s "%a),
        a,b = b, a+b
    print("\n")
fib(1000)
print("\n")
@

This example shows by that using the tool :doc:`lpEdit` we can embed Python or R code into these documents and the code will be executed when the website is created.

Reproducible research
----------------------

.. toctree::
   :maxdepth: 1

   ReproducibleResearch
   LiterateProgramming 
   Latex
   R
   Editor
    
Getting started with Sweave
-----------------------------

.. toctree::
   :maxdepth: 1

   Sweave
   SweaveExampleWalkThrough

Learning both R and LaTeX with Sweave
---------------------------------------------------------

.. toctree::
   :maxdepth: 1
 
   LearningR
   SweavePlots
   ImportCsvFiles