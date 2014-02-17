#!/usr/bin/python

'''
this script activates the GUI

A. Richards
'''

import sys, getopt, os, re
from PyQt4 import QtGui
#__currentdir__ = os.path.realpath(os.path.dirname(__file__))
#sys.path.append(os.path.join(__currentdir__,'lpEdit'))

from lpEdit import MainWindow

## check for the debug flag
try:
    optlist, args = getopt.getopt(sys.argv[1:],'f:d')
except getopt.GetoptError:
    print getopt.GetoptError
    print sys.argv[0] + "-f"
    print "Note: filePath (-f) flag to run the editor with a given input file"
    sys.exit()

debug = False
filePath = None
for o, a in optlist:
    if o == '-f':
        filePath = a
    if o == '-d':
        debug = True

if filePath != None and os.path.exists(filePath) != True:
    print "ERROR: invalid input file path starting with no input file"
    filePath = None

class Main():
    def __init__(self):
        app = QtGui.QApplication(sys.argv)
        app.setApplicationName("lpEdit")
        app.setWindowIcon(QtGui.QIcon('icon.png'))
        mw = MainWindow(debug=debug,filePath=filePath)
        mw.show()
        mw.raise_()
        app.exec_()

if __name__ == '__main__':
    main = Main()
