#!/usr/bin/env python
"""
cleans the documents build directory
builds and compiles all specified files

When building reST documentation a couple of things are important to remember

    (1) The first file in the list must be from the main project directory
    (2) If index.rst or conf.py are not present they will be created automatically
    (3) Only the files that have embedded code need to be listed

"""

import os,shutil
from lpedit import NoGuiAnalysis

## 
files = [('index.rst',None),
         ('ImportCsvFiles.rst','r'),
         ('LearningR.rst','r'),
         ('LiterateProgramming.rst','python'),
         (os.path.join('bayesian-course','BayesianDay1.rst'),'python'),
         (os.path.join('bayesian-course','BayesianPipeline.rst'),'r'),
         (os.path.join('bayesian-course','BayesianLinRegR.rst'),'r')
          ]

## clean first
if os.path.isdir("_sphinx"):
    shutil.rmtree("_sphinx")

## load files into project
nga = NoGuiAnalysis()
for filePath, language in files:
    nga.load_file(filePath,fileLang=language)

## build all the files
for filePath,language in files:
    fileName = os.path.split(filePath)[-1]
    if language != None:
        print 'BUILDING:', fileName
        nga.build(fileName=fileName)

## compile html
nga.compile_html()
