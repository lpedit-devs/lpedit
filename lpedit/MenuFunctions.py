#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,re,os
from PyQt4 import QtGui,QtCore
from basedir import __basedir__

def add_actions(mainWindow, target, actions):
    '''
    add menu actions    
    '''
    for action in actions:
        if action is None:
            target.addSeparator()
        else:
            target.addAction(action)

def create_action(mainWindow,text,slot=None,shortcut=None,icon=None,
                  tip=None,checkable=False,signal="triggered()"):   
    """
    create menu actions
    """

    action = QtGui.QAction(text,mainWindow)

    if icon is not None:
        iconPath = os.path.join(mainWindow.controller.baseDir,"icons",icon+".png")
        if os.path.isfile(iconPath) == True:
            action.setIcon(QtGui.QIcon(iconPath))
        else:
            print "WARNING: bad icon specified", icon + ".png"

    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot != None:
        mainWindow.connect(action, QtCore.SIGNAL(signal), slot)

    if checkable:
        action.setCheckable(True)

    #action.setEnabled(True)
    return action

def create_menubar_toolbar(mainWindow):

    '''
    create menubar where each toolbar contains the actions    
    '''

    ## file menu actions
    fileNewAction = create_action(mainWindow,"&New...",slot=mainWindow.transitions.move_to_new_project,
                                  shortcut=QtGui.QKeySequence.New,icon='filenew', tip="Create a new file")
    fileOpenAction = create_action(mainWindow,"&Open...", slot=mainWindow.open_file_callback,
                                   shortcut=QtGui.QKeySequence.Open, icon="fileopen",
                                   tip="Open an existing project")
    fileSaveAction = create_action(mainWindow,"&Save", slot=mainWindow.file_save,
                                   shortcut=QtGui.QKeySequence.Save, icon="filesave", tip="Save the document")
    fileSaveAsAction = create_action(mainWindow,"Save &As...",
                                     slot=mainWindow.file_save_as, icon="filesaveas",
                                     tip="Save the project using a new name")
    filePrintAction = create_action(mainWindow,"&Print", slot=mainWindow.file_print,
                                    shortcut=QtGui.QKeySequence.Print, icon="fileprint", tip="Print the current image")
    fileCloseAction = create_action(mainWindow,"&Close", slot=mainWindow.remove_tab,
                                    shortcut=QtGui.QKeySequence.Close,icon="fileclose", tip="Close the current tab")
    fileQuitAction = create_action(mainWindow,"&Quit", slot=mainWindow.close_app,
                                   shortcut=QtGui.QKeySequence.Quit, icon="filequit", tip="Close the application")
    ## edit menu actions
    editPreferencesAction = create_action(mainWindow,"&Preferences",slot=mainWindow.transitions.move_to_preferences,
                                          shortcut=QtGui.QKeySequence.Preferences, icon='preferences', tip="Application preferences")
  
    editSphinxPreferencesAction = create_action(mainWindow,"Sphinx Preferences",slot=mainWindow.transitions.move_to_sphinx_preferences,
                                                shortcut=None, icon='preferences', tip="Sphinx conf.py preferences")
  
    zoomInAction = create_action(mainWindow,"Zoom In",slot=mainWindow.transitions.zoom_in,
                                 shortcut=QtGui.QKeySequence.ZoomIn, icon='editzoom', tip="Zoom In")
    zoomOutAction = create_action(mainWindow,"Zoom Out",slot=mainWindow.transitions.zoom_out,
                                  shortcut=QtGui.QKeySequence.ZoomOut, icon='editzoom',tip="Zoom Out")
    msg = "Reload the editor tabs -- font size, highlighting etc"
    reloadAction  = create_action(mainWindow,"Refresh Tabs",slot=mainWindow.transitions.reload_tabs,
                                  shortcut=QtGui.QKeySequence.Refresh,icon='refresh',tip=msg)

    msg = "load all project files into the editor"
    showAllAction  = create_action(mainWindow,"Load Project Files",slot=mainWindow.transitions.load_project_files,
                                    shortcut=None,icon='fileopen',tip=msg)
    
    msg = "Build all files in a project"
    buildAllAction  = create_action(mainWindow,"Build All",slot=mainWindow.transitions.build_all,
                                    shortcut=None,icon='refresh',tip=msg)

    msg = "View embedded code output"
    viewOutputAction  = create_action(mainWindow,"View Code Output",slot=mainWindow.transitions.view_output,
                                      shortcut=None,icon='fileopen',tip=msg)

    ## help menu actions
    helpAboutAction = create_action(mainWindow,"&About %s"%mainWindow.appName,
                                    mainWindow.help_about)
    helpHelpAction = create_action(mainWindow,"&Help", mainWindow.generic_callback,
                                   QtGui.QKeySequence.HelpContents)

    ## define file menu
    fileMenu = mainWindow.menuBar().addMenu("&File")
    fileMenuActions = (fileNewAction,fileOpenAction,
                       fileSaveAction,fileSaveAsAction,None,
                       fileCloseAction,fileQuitAction)
    add_actions(mainWindow,fileMenu,fileMenuActions)

    ## define edit menu
    editMenu = mainWindow.menuBar().addMenu("&Edit")
    editMenuActions = [editPreferencesAction,editSphinxPreferencesAction,zoomInAction,zoomOutAction]
    add_actions(mainWindow,editMenu,editMenuActions)

    ## define tool menu
    toolMenu = mainWindow.menuBar().addMenu("&Tools")
    toolMenuActions = [reloadAction,showAllAction,buildAllAction,viewOutputAction]
    add_actions(mainWindow,toolMenu,toolMenuActions)

    ## define help menu
    helpMenu = mainWindow.menuBar().addMenu("&Help")
    add_actions(mainWindow,helpMenu,(helpAboutAction,helpHelpAction))
