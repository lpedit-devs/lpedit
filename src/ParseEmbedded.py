#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
(1) parce an input Rnw or reST file to get the Python chunks
(2) take the chunks and assemble them as a single file called chunks.py

inFileName is a file path to a *.rst | *.Rnw file
outFileName is a file path to a outfile name (i.e. chunks.py)

USAGE:
   
    $ python ParsePython.py -i foo.Rnw -o chunks.py

NOTE: this script preserves the order of the code chunks
"""

import getopt,sys,os,re

## parse inputs 
if len(sys.argv) < 5:
    print "INPUT ERROR", sys.argv[0] + " -i inFileName -o outFileName"
    sys.exit()

try:
    optlist, args = getopt.getopt(sys.argv[1:],'i:o:')
except getopt.GetoptError:
    print getopt.GetoptError
    print "INPUT ERROR:", sys.argv[0] + "-i inFileName -o outFileName"
    sys.exit()

inFileName = None
outFileName = None

for o, a in optlist:
    if o == '-i':
        inFileName = a
    if o == '-o':
        outFileName = a

## error checking
if os.path.exists(inFileName) == False:
    print "INPUT ERROR:", sys.argv[0], inFileName, "does not exist"
    sys.exit()

if not re.search("\.rnw|\.rst|\.nw",inFileName,flags=re.IGNORECASE):
    print "INPUT ERROR:", sys.argv[0], inFileName, "in file not of type *.Rnw or *.rst"
    sys.exit()

print "extracting code from file...", inFileName

## open a file
outFileHandle = open(outFileName,'w')
inFileHandle = open(inFileName,'r')
isNoweb = False

## ensure parent dir is in path in python
if re.search("\.py",outFileName):
    outFileHandle.write("import sys\nsys.path.append('..')\n")

for linja in inFileHandle:

    if re.search('^<<.+>>=',linja):
        isNoweb = True

    if isNoweb == True:
        if re.search('^<<.+>>=',linja):
            outFileHandle.write("print('%s')\n"%re.sub("\s+","",linja))
            outFileHandle.write("print('...')\n")
        elif re.search('^@',linja):
            outFileHandle.write("print('%s')\n"%re.sub("\s+","",linja))
        else:
            outFileHandle.write(linja)
        
    if re.search('^\@',linja):
        isNoweb = False
