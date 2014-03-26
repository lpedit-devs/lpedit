#!/usr/bin/env python
"""
cleans the documents build directory
builds and compiles all specified files

"""

import os,shutil
from lpedit import NoGuiAnalysis


## note that you have to load a file from the main project directory first
files = [('index.rst',None),
         (os.path.join('bayesian-course','BayesianDay1.rst'),'python')
         ]
nga = NoGuiAnalysis()

## clean first
if os.path.isdir("_sphinx"):
    shutil.rmtree("_sphinx")

## load files into project
for fileName, language in files:
    print fileName, language
    nga.load_file(fileName,fileLang=language)

## build all the files
for fileName,language in files:
    if language != None:
        nga.build(fileName=fileName)

