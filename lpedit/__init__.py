import sys,os

## files requiring no other dep
from version import __version__
from basedir import __basedir__
from SphinxLogger import SphinxLogger
from RunSubprocess import RunSubprocess
from Controller import Controller
from NoGuiAnalysis import NoGuiAnalysis
from MenuFunctions import create_menubar_toolbar,create_action,add_actions
from Preferences import Preferences
from NewProject import NewProject
from TextScreen import TextScreen
from ButtonDock import ButtonDock
from QSciEditor import QSciEditor
from MainWindow import MainWindow
from lpEdit import Main
