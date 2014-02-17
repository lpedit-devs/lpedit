"""
get the base directory for lpedit
"""

import sys,os,re

if hasattr(sys,'frozen'):
    __basedir__ = os.path.dirname(sys.executable)
    __basedir__ = re.sub("MacOS","Resources",__basedir__)
else:
    __basedir__ = os.path.realpath(os.path.dirname(__file__))

#if os.path.split(__basedir__)[-1] != "lpEdit":
#    __basedir__ = os.path.join(__basedir__,"lpEdit")
    
if os.path.isdir(os.path.join(__basedir__,'lpEdit')) == True:
    __basedir__ = os.path.join(__basedir__,"lpEdit")
