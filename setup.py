#!/usr/bin/env python
                
import os,sys,re

from distutils.core import setup
try:
    from py2exe.build_exe import py2exe
except:
    pass

from numpy import get_include

sys.path.append("lpedit")
from version import __version__

DESCRIPTION = "Cross-platform editor to facilitate literate programming"
LONG_DESCRIPTION = """
lpEdit is an application written in PyQt4 that and based on QScintilla.

It implements a simple framework for writing Sweave documents.  The project
will be extended to other literate programming paradigms in the near future.

Notes
-----
Installation from source requires
 
  * qscintilla2 
  * qt4 
  * numpy
  * matplotlib
  * sphinx
"""

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

ISRELEASED = True
VERSION = __version__
FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.beta'

def get_files(dirPath):
    notIncluded = ["\.pyc"]
    allFiles = []
    for fileName in os.listdir(dirPath):
        include = True
        for pat in notIncluded:
            if re.search(pat,fileName):
                include = False
        if include == True:
            allFiles.append(os.path.join(dirPath,fileName))
    return allFiles

if __name__ == '__main__':
    setup(name=DISTNAME,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          description=DESCRIPTION,
          version=FULLVERSION,
          license=LICENSE,
          url=URL,
          packages=['lpedit','lpedit.icons','lpedit.templates',
                    'lpedit.examples','lpedit.styfiles','lpedit.sphinxfiles'],
          options={
            "py2exe":{
                "unbuffered": True,
                "includes":["sip"],
                "optimize": 2,}},
          #windows=[{"script":"lpEditStart.py"}],
          long_description=LONG_DESCRIPTION,
          classifiers=CLASSIFIERS,
          data_files = [('icons',get_files(os.path.join('lpedit','icons'))),
                        ('styfiles',get_files(os.path.join('lpedit','styfiles'))),
                        ('sphinxfiles',get_files(os.path.join('lpedit','sphinxfiles'))),
                        ('examples',get_files(os.path.join('lpedit','examples'))),
                        ('templates',get_files(os.path.join('lpedit','templates')))],
          platforms='any')
