"""
get the base directory for lpedit
"""

import sys,os,re

if hasattr(sys,'frozen'):
    __basedir__ = os.path.dirname(sys.executable)
    __basedir__ = re.sub("MacOS","Resources",__basedir__)
else:
    __basedir__ = os.path.abspath(os.path.dirname(__file__))
    
#if os.path.isdir(os.path.join(__basedir__,'lpedit')) == True:
#    __basedir__ = os.path.join(__basedir__,"lpedit")
