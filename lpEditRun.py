#!/usr/bin/python

'''
this script runs lpedit without a gui

A. Richards
'''

import sys, getopt, os
from PyQt4 import QtGui
sys.path.append(os.path.join(os.getcwd(),'lpedit'))
from lpedit import NoGuiAnalysis

def print_help():
    print "\n"
    print sys.argv[0] + " -f -c -l"
    print "filePath (-f) flag to run the editor with a given input file"
    print "language (-l) usually 'python' or 'r'"
    print "compile-type (-c) either pdf or html"
    print "\nfor example..."
    print "\n$~ python lpEditRun.py -f foo.rst -c html -l python"
    print "\n"

## check for the debug flag
try:
    optlist, args = getopt.getopt(sys.argv[1:],'f:l:c:h')
except getopt.GetoptError:
    print getopt.GetoptError
    print_help()
    sys.exit()

debug = False
filePath = None
compileType = None
language = 'python'

for o, a in optlist:
    if o == '-f':
        filePath = a
    if o == '-l':
        language = a
    if o == '-c':
        compileType = a
    if o == '-h':
        print_help()
        sys.exit()

## error checking
if filePath == None:
    print "\nSYNTAX ERROR:" + sys.argv[0] + " -f -c -l"
    print "\tfilePath (-f) is a required input\n"
    sys.exit()
if compileType != None:
    compileType = compileType.lower()
if compileType not in ['pdf','html']:
    print "\nSYNTAX ERROR:" + sys.argv[0] + " -f -c"
    print "\tcompileType (-c) is a required input and must be either 'pdf' or 'html'"
    print "\t'%s' is invalid\n"%str(compileType)
    sys.exit()
if filePath != None and os.path.exists(filePath) != True:
    print "\nSYNTAX ERROR: invalid input file path specified -- does not exist"
    sys.exit()
if language != None:
    language = language.lower()
if language not in ['r','python']:
    print "\nSYNTAX ERROR: invalid language specified"
    sys.exit()
    
if __name__ == '__main__':
   nga = NoGuiAnalysis()
   nga.load_file(filePath,fileLang=language)
   goFlag = nga.build()
   print goFlag

   if goFlag != True:
       print "Skipping output compile."
       sys.exit()

   if compileType == 'pdf':
       nga.compile_pdf()
       print "pdf output ready"
   else:
       nga.compile_html()
       print "html output ready"
