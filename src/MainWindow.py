#!/usr/bin/env python
# -*- coding: utf-8 -*- 

"""
MainWindow widget for lpEdit

  This program or module is free software: you can redistribute it and/or
  modify it under the terms of the GNU General Public License as published
  by the Free Software Foundation version 3 of the License, or 
  (at your option) any later version. It is provided for educational purposes 
  and is distributed in the hope that it will be useful, but WITHOUT ANY 
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
  FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

  Adam Richards
  adamricha@gmail.com
"""

import os,sys,platform,re
from PyQt4 import QtCore, QtGui, Qsci
from PyQt4.QtCore import PYQT_VERSION_STR, QT_VERSION_STR
from Transitions import Transitions
from Controller import Controller
from NoGuiAnalysis import NoGuiAnalysis
from MenuFunctions import create_menubar_toolbar 
from ButtonDock import ButtonDock

__author__ = "AJ Richards"

newWindowText = "Welcome to lpEdit\nTo begin click on file -> new or file -> open"

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None,debug=False,filePath=None):
        """
        MainWindow constructor
        """

        QtGui.QMainWindow.__init__(self)

        ## variables
        self.appName = "lpEdit"
        self.controller = Controller(debug=debug)
        self.nga = NoGuiAnalysis(self.controller,mainWindow=self)
        self.setWindowTitle(self.appName)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.screenWidth = screen.width()
        self.screenHeight = screen.height()
        self.mainWidget = QtGui.QWidget(self)
        self.preferences = None
        self.progressBar = None
        self.sphinxLogs = {}
        self.newProject = None
        self.tabWidget = None
        self.titleLabel = None
        self.unsaved = []

        ## initialize widgets
        self.controller.reset_all()
        self.init_button_dock()
     
        ## initialize all main widgets
        self.transitions = Transitions(self)

        ## initialize menu bar
        create_menubar_toolbar(self)

        ## ensure we have absolute file path
        if filePath != None:
            filePath =  os.path.realpath(filePath)

        if filePath == None:
            self.transitions.move_to_logo()
        elif filePath != None and os.path.exists(filePath) == False:
            print "WARNING: MainWindow -- invalid file path specified as input"
            print 'skipping...'
        else:
            self.transitions.add_new_editor_tab(filePath)
            self.transitions.move_to_editor()
            
        ## finalize layout
        self.show()
        self.showMaximized()

    def load_file(self,filePath,fileLang=None):
        '''
        load a given file path both for the controller and the tabs
        load file is called when a tab widget is already present 
        '''

        ## ensure we have absolute file path 
        if filePath != None:
            filePath = os.path.realpath(filePath)

        ## ensure the path exists
        if filePath == None or os.path.exists(filePath) == False:
            print "WARNING: MainWindow.load_file -- bad file path specified"
            print "...", filePath
            return

        ## ensure the file is not already loaded
        if filePath in self.controller.filePathList:
            errMsg = "Cannot load file: file of same name is already loaded"
            self.display_warning(errMsg)
            return

        ## ensure we do not have more than the max number of documents
        numActive = self.controller.get_number_active_files()
        if int(numActive) == int(self.controller.maxDocuments):
            self.display_info("The maximum number of documents are open\nClose a document an then try again")
            return
        
        ## load files
        self.nga.load_file(filePath,fileLang=fileLang)
        
    def ensure_tab_is_current(self):
        """
        action to take on user changing current file index
        """

        currentIndex = self.tabWidget.currentIndex()
    
        self.controller.currentFileIndex = currentIndex
        fileLang = self.controller.fileLangList[currentIndex]
        fileName = self.controller.fileNameList[currentIndex]
        
        if str(fileName) == 'None':
            return
            

        if re.search("\.rnw|\.nw",fileName,flags=re.IGNORECASE):
            reportType = "PDF"
        else:
            reportType = "HTML"
        self.bDock.reportSelector.setCurrentIndex(self.bDock.reportList.index(reportType))

        if fileLang != None:
            self.bDock.langSelector.setCurrentIndex(self.bDock.langList.index(fileLang))

    def remove_tab(self,fileName=None):
        """
        removes a tab from self.tabWidget and calls appropriate cleanup functions
        """

        if self.transitions.isEditor == False:
            return

        if fileName not in self.controller.fileNameList:
            print "ERROR: MainWindow -- trying to remove invalid tab fileName"
            return

        if fileName == None:
            currentIndex = self.tabWidget.currentIndex()
            fileName = self.controller.fileNameList[currentIndex]

        indexToRemove = self.controller.fileNameList.index(fileName)
        self.tabWidget.removeTab(indexToRemove)
        self.controller.remove_file(fileName)
        #self.ensure_tab_is_current()
        self.transitions.move_to_editor()


    def create_statusbar(self):
        """
        create the bottom status bar
        """

        self.sizeLabel = QtGui.QLabel()
        self.sizeLabel.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        self.status = self.statusBar()
        self.status.setSizeGripEnabled(False)
        self.status.addPermanentWidget(self.sizeLabel)
        self.status.showMessage("Ready", 5000)

    def init_button_dock(self):
        """
        initialize the button dock
        """

        self.buttonDock = QtGui.QDockWidget(self)
        self.buttonDock.setObjectName("ButtonDockWidget")
        self.buttonDock.setAllowedAreas(QtCore.Qt.TopDockWidgetArea|QtCore.Qt.BottomDockWidgetArea)
        self.bDock = ButtonDock(mainWindow=self,buttonSize=0.09*self.screenWidth)

        hbl1 = QtGui.QHBoxLayout()
        hbl1.setAlignment(QtCore.Qt.AlignLeft)
        hbl1.addWidget(self.bDock)
        vbl = QtGui.QHBoxLayout()
        vbl.addLayout(hbl1)
        vbl.setAlignment(QtCore.Qt.AlignLeft)

        self.buttonDock.setWidget(self.bDock)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.buttonDock)
        self.buttonDock.setMaximumHeight(0.09 * self.screenHeight)

    def set_editing_mode(self):
        '''
        adds a star when editing doc
        '''

        self.ensure_tab_is_current()
        fileIndex = self.controller.currentFileIndex
        editor = self.controller.editorList[fileIndex]
        fileName = self.controller.fileNameList[fileIndex]
        
        if fileName == None:
            return

        if fileName not in self.unsaved:
            self.tabWidget.setTabText(fileIndex,fileName+"*")
            self.unsaved.append(fileName)

    def help_about(self):
        """
        Function to display help information
        """

        QtGui.QMessageBox.about(self, "About %s"%self.appName,
                                """<b>%s</b> v %s
                                <p>About:This application can be used to perform
                                literate programming via Sweave and Sphinx.
                                <p>License: <a href='http://www.gnu.org/licenses/gpl-3.0.txt'>The GNU General Public License v3.0</a>  
                                <p>Development: 
                                <a href='http://bitbucket.org/ajrichards/reproducible-research'>http://bitbucket.org/ajrichards/reproducible-research</a> 
                                <p>Documentation: 
                                <a href='http://ajrichards.bitbucket.org/lpEdit/index.html'>http://ajrichards.bitbucket.org/lpEdit/index.html</a> 
                                <p>Python %s
                                <p>Qt     %s
                                <p>PyQt   %s  
                                <p>System %s
                                """ % (self.appName,
                                       self.controller.version, platform.python_version(),
                                       QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def open_file_callback(self):
        """
        callback function to open a *.nw, *.rnw or *.rst file
        """

        defaultDir = os.getcwd()

        
        
        fileFilter = "*.rst;;*.rnw;;*.nw;;*"

        inputFilePath = QtGui.QFileDialog.getOpenFileName(self,'Open file(s)',defaultDir,fileFilter)

        ## return if user aborts
        if inputFilePath == '':
            return

        inputFilePath = str(inputFilePath)
        if not re.search("\.rst|\.Rnw|\.rnw|\.nw",os.path.split(inputFilePath)[-1]):
            errMsg = "loaded file is of unknown extension\n" + inputFilePath
            print "WARNING: ", errMsg 
            self.display_warning(errMsg)
            return

        self.transitions.add_new_editor_tab(inputFilePath)
        self.transitions.move_to_editor()

        ## move to opened tab
        newIndex = self.controller.fileNameList.index(os.path.split(inputFilePath)[-1])
        self.tabWidget.setCurrentIndex(newIndex)
        self.ensure_tab_is_current()


    def _file_save(self,fileIndex):
        """
        lpEdits internal file save
        """

        fileName = self.controller.fileNameList[fileIndex]
        filePath = self.controller.filePathList[fileIndex]
        editor = self.controller.editorList[fileIndex]
        currentText = editor.get_text()
        fid = open(filePath,'w')
        
        ## remove carriage returns
        if re.search("\r",currentText):
            currentText = re.sub("\r+","",currentText)

        fid.write(currentText)
        fid.close()

    def file_save(self,display=True):
        '''
        saves the file in the current tab as itself
        '''

        self.ensure_tab_is_current()
        fileIndex = self.controller.currentFileIndex
        if self.controller.fileNameList[fileIndex] == None:
            self.display_info("A valid file must be loaded before saving")
            return

        templatesDir = self.controller.get_templates_dir()
        currentFilePath = self.controller.filePathList[fileIndex]
        currentFileName = self.controller.fileNameList[fileIndex]
        if os.path.join(templatesDir,currentFileName) == currentFilePath:
            self.display_info("Cannot overwrite template -- use 'Save As'")
            return

        self._file_save(fileIndex)

        fileName = self.controller.fileNameList[fileIndex]
        if fileName in self.unsaved:
            self.unsaved.remove(fileName)
            self.tabWidget.setTabText(fileIndex,fileName)

        if display == True:
            self.display_info("Progress saved")

    def file_save_as(self):
        """
        saves the file in the current tab as another file
        """

        self.ensure_tab_is_current()
        if self.controller.fileNameList[self.controller.currentFileIndex] == None:
            self.display_info("A valid file must be loaded before saving")
            return

        currentFilePath = self.controller.filePathList[self.controller.currentFileIndex]
        currentFileName = self.controller.fileNameList[self.controller.currentFileIndex]
        currentEditor = self.controller.editorList[self.controller.currentFileIndex]
        currentText = currentEditor.get_text()

        defaultDir = os.path.split(currentFilePath)[0]
        if re.search("\.rnw",currentFileName,flags=re.IGNORECASE):
            fileFilter = "*.rnw;;*.Rnw"
        elif re.search("\.nw",currentFileName,flags=re.IGNORECASE):
            fileFilter = "*.nw"
        else:
            fileFilter = "*.rst"
      
        newFilePath, extension = QtGui.QFileDialog.getSaveFileNameAndFilter(self,'Save As',defaultDir,fileFilter)
        newFilePath = str(newFilePath)
        
        if newFilePath == '':
            return

        ## if user does not provide an extension then default to template ext
        if not re.search("\.rnw|\.nw|\.rst",newFilePath,flags=re.IGNORECASE):
            if  re.search("\.rnw",currentFileName,flags=re.IGNORECASE):
                newFilePath = newFilePath + ".rnw"
            elif  re.search("\.nw",currentFileName,flags=re.IGNORECASE):
                newFilePath = newFilePath + ".nw"
            else:
                newFilePath = newFilePath + ".rst"
                
        ## ensure file extension is valid
        if not re.search("\.rnw|\.nw|\.rst",newFilePath,flags=re.IGNORECASE):
            msg = "lpEdit only works with *.rnw, *.nw and *.rst files"
            msg += "You may resave using the appropriate extension"
            self.display_warning(msg)
            return
    
        ## ensure that user preserves file extension
        msg = "To save you must preserve the file extension<p>"
        msg += "e.g. a *.rst file must be saved as a *.rst file<p>"
        msg += "Use a different template if necessary"
        if re.search("\.rnw",newFilePath,flags=re.IGNORECASE) and not re.search("\.rnw",currentFileName,flags=re.IGNORECASE):
            self.display_warning(msg)
            return
        if re.search("\.rst",newFilePath,flags=re.IGNORECASE) and not re.search("\.rst",currentFileName,flags=re.IGNORECASE):
            self.display_warning(msg)
            return
        if re.search("\.nw",newFilePath,flags=re.IGNORECASE) and not re.search("\.nw",currentFileName,flags=re.IGNORECASE):
            self.display_warning(msg)
            return

        fid = open(newFilePath,'w')
        fid.write(currentText)
        fid.close()

        ## load the new file
        self.transitions.add_new_editor_tab(newFilePath)
        self.transitions.move_to_editor()

        ## remove the old tab
        #self.remove_tab(currentFileName)

        newIndex = self.controller.fileNameList.index(os.path.split(newFilePath)[-1])
        self.tabWidget.setCurrentIndex(newIndex)
        self.ensure_tab_is_current()

        self.display_info("File saved")

    def file_print(self):
        self.display_info("This function is not yet implemented")
    
    def display_info(self,msg):
        """
        display info via a message box
        generic function to display info to user
        """
        reply = QtGui.QMessageBox.information(self,'Information',msg)

    def display_warning(self,msg):
        """
        display warning via a message box
        generic function to display a warning to user
        """
        reply = QtGui.QMessageBox.warning(self, "Warning", msg)

    def close_app(self):
        """
        callback function to close lpEdit
        asks user about saving if there are unsaved docs open
        """
        
        if len(self.unsaved) == 0:
            self.close()
            return
            
        reply = QtGui.QMessageBox.question(self, self.controller.appName,
                                           "There are unsaved files are you sure you want to exit?", 
                                           QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.close()
            return

    def generic_callback(self):
        self.display_info("This function is not yet implemented")
