#!/usr/bin/env python
                
import os,sys,re

#from numpy.distutils.misc_util import Configuration
#from numpy.distutils.core import setup

from distutils.core import setup
try:
    from py2exe.build_exe import py2exe
except:
    pass

sys.path.append("lpEdit")
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

#REQUIRES = ['numpy', 'pycuda >= 0.94rc']
REQUIRES = ['numpy', 'matplotlib','PyQt4','QSciEditor','sphinx']
DISTNAME = 'lpEdit'
LICENSE = 'GNU GPL v3'
AUTHOR = "Adam J Richards"
AUTHOR_EMAIL = "adamricha@gmail.com"
URL = 'https://bitbucket.org/ajrichards/reproducible-research'
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

#def configuration(parent_package='', top_path=None):
#    config = Configuration(None, parent_package, top_path,
#                           version=FULLVERSION)
#    config.set_options(ignore_setup_xxx_py=True,
#                       assume_default_configuration=True,
#                       delegate_options_to_subpackages=True,
#                       quiet=True)
#
#    config.add_subpackage('lpEdit')
#    config.add_data_dir(os.path.join('lpEdit','icons'))
#    config.add_data_dir(os.path.join('lpEdit','styfiles'))
#    config.add_data_dir(os.path.join('lpEdit','examples'))
#    config.add_data_dir(os.path.join('lpEdit','templates'))
#    config.add_data_dir(os.path.join('lpEdit','sphinxfiles'))
#
#    return config

def get_data_files(dirPath):
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
          license=LICENSE,
          url=URL,
          zipfile = None,          
          packages=['lpEdit','lpEdit.icons','lpEdit.templates',
                    'lpEdit.examples','lpEdit.styfiles','lpEdit.sphinxfiles'],
          options={
            "py2exe":{
                "unbuffered": True,
                "includes":["sip"],
                "optimize": 2,}},
          windows=[{"script":"lpEditStart.py"}],
          long_description=LONG_DESCRIPTION,
          classifiers=CLASSIFIERS,
          data_files = [('icons',get_data_files(os.path.join('lpEdit','icons'))),
                        ('styfiles',get_data_files(os.path.join('lpEdit','styfiles'))),
                        ('sphinxfiles',get_data_files(os.path.join('lpEdit','sphinxfiles'))),
                        ('examples',[os.path.join('lpEdit','examples','README.txt')]),
                        ('templates',get_data_files(os.path.join('lpEdit','templates')))],
    
          platforms='any')

##############
'''
setup(name='lpEdit',
      version='0.1',
      description='A cross-platform editor to facilitate literate programming',
      author='Adam J Richards, ',
      author_email='adamricha@gmail.com',
      package_dir = {'lpEdit':'src','lpEdit.icons':os.path.join('src','icons'),'lpEdit.examples':'examples'},
      packages=['lpEdit','lpEdit.icons','lpEdit.examples'],
      url='https://bitbucket.org/ajrichards/reproducible-research',
      long_description = '',
      license='GNU GPL v3',
      )
'''
