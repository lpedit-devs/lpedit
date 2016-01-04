lpedit
======

lpEdit is a editor for literate programming in R and Python through the use of LaTeX and reStructuredText.  This tool helps make statistical analyses more reproducible. 

See the documentation for instructions on installation.

After installation lpedit may simple be started from the terminal with the command 'lpEdit.py'.

To create a document with Python:

>>> from lpedit import NoGuiAnalysis
>>> fileName = 'report-name.nw'
>>> language = 'python'
>>> nga = NoGuiAnalysis()
>>> nga.load_file(fileName,fileLang=language)
>>> nga.build(fileName)
>>> nga.compile_pdf()
