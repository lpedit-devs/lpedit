#!/usr/bin/env python
                
import os,sys,re
from distutils.sysconfig import get_python_lib
from shutil import copytree

#from distutils.core import setup
from numpy.distutils.core import setup

try:
    from py2exe.build_exe import py2exe
except:
    pass

## get version
sys.path.append("lpedit")
from version import __version__

DESCRIPTION = "Cross-platform editor to facilitate literate programming"
LONG_DESCRIPTION = """
lpEdit is an application written in PyQt4 that and based on QScintilla.

The environment enables a simple framework for writing reST or LaTeX documents that have  
either R or Python code embedded within.  These documents are
compilied and the code and results are integrated into the output document in a reproducible manner.

Notes
-----
Installation from source requires
 
  * qscintilla2 
  * qt4 
  * numpy
  * matplotlib
  * sphinx
"""

def get_files(dirPath):
    notIncluded = ["\.pyc"]
    allFiles = []
    for fileName in os.listdir(dirPath):
        include = True
        for pat in notIncluded:
            if re.search(pat,fileName):
                include = False
        filePath = os.path.join(dirPath,fileName)
        if include == True and os.path.isfile(filePath):
            allFiles.append(os.path.realpath(filePath))
            
    return allFiles

REQUIRES = ['numpy', 'matplotlib','PyQt4','QSciEditor','sphinx']
DISTNAME = 'lpedit'
LICENSE = 'GNU GPL v3'
AUTHOR = "Adam J Richards"
AUTHOR_EMAIL = "adamricha@gmail.com"
URL = 'https://github.com/lpedit-devs/lpedit'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: X11 Applications :: Qt'
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
]

DATADIRS = ["icons","styfiles","sphinxfiles","examples","templates"]

FILES = {'': [os.path.join("lpedit","*.py")],
         'icons': [os.path.join("lpedit","icons","*.png")],
         'styfiles': [os.path.join("lpedit","styfiles","*.sty")],
         'sphinxfiles': [os.path.join("lpedit","sphinxfiles","*.py *.rst")],
         'examples': [os.path.join("lpedit","examples","*.rnw *.nw *.rst")],
         'templates':[os.path.join("lpedit","templates","*.rnw *.nw *.rst")]}

ISRELEASED = True
VERSION = __version__
FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.beta'

if __name__ == '__main__':
    setup(name=DISTNAME,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          description=DESCRIPTION,
          version=FULLVERSION,
          license=LICENSE,
          url=URL,
          packages=['lpedit'],
          scripts=[os.path.join("lpedit","lpEdit.py")],
          windows=[{"script":os.path.join("lpedit","lpEdit.py")}],
          long_description=LONG_DESCRIPTION,
          classifiers=CLASSIFIERS,
          options={"py2exe": {"skip_archive": True, "includes": ["sip"]}},
          package_data= FILES,
         
          data_files = [
            (os.path.join('lpedit','icons'),get_files(os.path.join('lpedit','icons'))),
            (os.path.join('lpedit','styfiles'),get_files(os.path.join('lpedit','styfiles'))),
            (os.path.join('lpedit','sphinxfiles'),get_files(os.path.join('lpedit','sphinxfiles'))),
            (os.path.join('lpedit','examples'),get_files(os.path.join('lpedit','examples'))),
            (os.path.join('lpedit','templates'),get_files(os.path.join('lpedit','templates')))],
          platforms='any')
