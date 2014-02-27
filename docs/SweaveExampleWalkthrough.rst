.. reproducible research tutorial file, created by ARichards

==========================
Sweave example walkthrough
==========================

The example file can be downloaded:: :download:`FishersExactTest.Rnw  </../lpedit/examples/FishersExactTest.Rnw>`

This first section is the preable to your LaTeX document.  Do not forget to include the highlighted package in 
your Sweave document.

.. literalinclude:: /../../lpedit/examples/FishersExactTest.Rnw
   :language: latex
   :emphasize-lines: 3
   :lines: 1-5

The next block of the code simply begins the LaTeX document and specifies a section start in the standard way.

.. literalinclude:: /../../lpedit/examples/FishersExactTest.Rnw
   :language: latex
   :lines: 6-13

Then we specify a table in LaTeX.  Still there has been no mention of R or Sweave.

.. literalinclude:: /../../lpedit/examples/FishersExactTest.Rnw
   :language: latex
   :lines: 15-25

Finally, we include our first bit of code in the documents.  Notice that the R code is bookended by 
**<<data>>=** and **@**.  The variable *data* is a reference name for the code block.

.. literalinclude:: /../../lpedit/examples/FishersExactTest.Rnw
   :language: latex
   :emphasize-lines: 1,6
   :lines: 27-32

The last section is where we actually run the test and print the result.  Again, the code is bookended in the same 
way and this time we label the code block *test*.

.. literalinclude:: /../../lpedit/examples/FishersExactTest.Rnw
   :language: latex
   :lines: 34-40
