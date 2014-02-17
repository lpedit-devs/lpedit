#!/usr/bin/python

'''
lpEdit
StateTransitions

functions that handle the transitions from one software state to another          

'''

__author__ = "A Richards"

import os,sys,re
from PyQt4 import QtGui,QtCore
from Preferences import Preferences
from QSciEditor import QSciEditor
from NewProject import NewProject
from BasicWidgets import Imager,ProgressBar
from SphinxLogger import SphinxLogger
from SphinxLoggerUI import SphinxLoggerUI
from NoGuiAnalysis import NoGuiAnalysis
from DocumentViewer import DocumentViewer

class Transitions():
    """
    class that handles the transitions between states
    """


    def __init__(self,mainWindow):
        """
        constructor initializes all widgets
        """

        ## variables
        self.mainWindow = mainWindow
        self.isEditor = False
        templatesDir = self.mainWindow.controller.get_templates_dir()
        self.mainWindow.workspace = QtGui.QWorkspace()
        self.mainWindow.workspace.setWindowTitle(self.mainWindow.appName)

        ## initialize main widgets
        img = os.path.join(self.mainWindow.controller.baseDir,"icons","logo.png")
        self.mainWindow.logoWidget = Imager(img)
        self.mainWindow.logoWidget.setVisible(False)
        self.mainWindow.workspace.addWindow(self.mainWindow.logoWidget)
        
        self.mainWindow.preferences = Preferences(mainWindow=self.mainWindow)
        self.mainWindow.preferences.setVisible(False)
        self.mainWindow.workspace.addWindow(self.mainWindow.preferences)
        
        self.mainWindow.newProject = NewProject(templatesDir,mainWindow=self.mainWindow)
        self.mainWindow.newProject.setVisible(False)
        self.mainWindow.workspace.addWindow(self.mainWindow.newProject)

        self.mainWindow.tabWidget = QtGui.QTabWidget()
        self.mainWindow.connect(self.mainWindow.tabWidget,QtCore.SIGNAL("currentChanged(int)"),
                                self.mainWindow.ensure_tab_is_current)
        self.mainWindow.tabWidget.setVisible(False)
        self.mainWindow.workspace.addWindow(self.mainWindow.tabWidget)

        ## finalize ui init
        self.mainWindow.setCentralWidget(self.mainWindow.workspace)
        self.mainWindow.workspace.cascade()
        self.move_to_logo()

    def hide_all(self):
        if self.mainWindow.logoWidget != None:
            self.mainWindow.logoWidget.hide()
        if self.mainWindow.preferences != None:
            self.mainWindow.preferences.hide()
        if self.mainWindow.tabWidget != None:
            self.mainWindow.tabWidget.hide()
        if self.mainWindow.newProject !=None:
            self.mainWindow.newProject.hide()

        for sphinxLog in self.mainWindow.sphinxLogs.itervalues():
            sphinxLog.hide()

    def move_to_logo(self):
        """
        transition to the initial widget
        """
        
        self.isEditor = False

        self.hide_all()
        self.mainWindow.bDock.use_welcome_mode()
        self.mainWindow.logoWidget.show()
        self.mainWindow.logoWidget.showMaximized()
        
    def update_ui(self):
        QtGui.QApplication.processEvents()
  
    def reload_tab(self,tab):
        """
        reloads a single tab where tab is the index (int)
        """

        ## error check
        if tab not in range(len(self.mainWindow.controller.fileNameList)):
            return

        fileName = self.mainWindow.controller.fileNameList[tab]
        if fileName == None:
            return

        self.mainWindow._file_save(tab)

        editor = self.mainWindow.controller.editorList[tab]
        currentText = editor.get_text()
        editor.load_text(currentText)

        ## remove the asterisk
        if fileName in self.mainWindow.unsaved:
            self.mainWindow.unsaved.remove(fileName)
        self.mainWindow.tabWidget.setTabText(tab,fileName)

    def start_waiting(self):
        """
        start wait for user
        """
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    def stop_waiting(self):
        """
        stop wait for user
        """

        QtGui.QApplication.restoreOverrideCursor()

    def reload_tabs(self):
        """
        reloads the text on all of the present editors
        """ 
        
        numActive = self.mainWindow.controller.get_number_active_files()

        if numActive == 0:
            self.move_to_logo()
            return

        toLoad = []
        for tab in range(len(self.mainWindow.controller.fileNameList)):
            self.reload_tab(tab)

    def move_to_editor(self):
        """
        move to the editor view
        """

        self.isEditor = True

        numActive = self.mainWindow.controller.get_number_active_files()
        if numActive == 0:
            self.move_to_logo()
            return
                
        self.hide_all()
        self.mainWindow.bDock.use_editor_mode()
        self.mainWindow.tabWidget.show()
        self.mainWindow.tabWidget.showMaximized()

    def add_new_editor_tab(self,filePath,fileLang=None):
        """
        after a new file is loaded (MainWindow.load_file)
        this convenience function is used to add a new tab
        """

        if filePath == None or os.path.exists(filePath) == False:
            print "ERROR: transitions.add_new_editor_tab -- bad specified file path"
            print "...", filePath
            #self.move_to_editor()
            return

        unsavedDocs = self.mainWindow.unsaved[:]

        ## load the file into lpEdit
        self.mainWindow.load_file(filePath,fileLang=fileLang)

        ## error checking
        numActive = self.mainWindow.controller.get_number_active_files()
        if numActive == 0:
            print "WARNING: transitions.add_new_editor_tab -- no active files loaded"
            return

        tab = numActive - 1
        if  self.mainWindow.controller.editorList[tab] != None:
            print "WARNING: transitions.add_new_editor_tab -- tab %s already exists"%tab
            return
            
        ## initialize editor
        fileName = self.mainWindow.controller.fileNameList[tab]
        filePath = self.mainWindow.controller.filePathList[tab]
        fileLang = self.mainWindow.controller.fileLangList[tab]
        self.mainWindow.controller.editorList[tab] = QSciEditor(mainWindow=self.mainWindow) 
        editor = self.mainWindow.controller.editorList[tab]
        self.mainWindow.tabWidget.addTab(editor,fileName)

        ## ensure edit star is off
        for fileIndex,fileName in enumerate(self.mainWindow.controller.fileNameList):
            if fileName in self.mainWindow.unsaved and fileName not in unsavedDocs:
                self.mainWindow.unsaved.remove(fileName)
                self.mainWindow.tabWidget.setTabText(fileIndex,fileName)

        ## move to new file
        self.mainWindow.tabWidget.setCurrentIndex(tab)
        editor.load_text(filePath)
        editor.set_lexer(fileName=filePath)
        self.mainWindow.ensure_tab_is_current()

        ## ensure edit star is off
        for fileIndex,fileName in enumerate(self.mainWindow.controller.fileNameList):
            if fileName in self.mainWindow.unsaved and fileName not in unsavedDocs:
                self.mainWindow.unsaved.remove(fileName)
                self.mainWindow.tabWidget.setTabText(fileIndex,fileName)


    def zoom_in(self):
        """
        zoom in
        """

        self.move_to_editor()
        self.mainWindow.ensure_tab_is_current()
        fileIndex = self.mainWindow.controller.currentFileIndex
        editor = self.mainWindow.controller.editorList[fileIndex]
        editor.zoom_in()

    def zoom_out(self):
        """
        zoom out
        """

        self.move_to_editor()
        self.mainWindow.ensure_tab_is_current()
        fileIndex = self.mainWindow.controller.currentFileIndex
        editor = self.mainWindow.controller.editorList[fileIndex]
        editor.zoom_out()
        
    def move_to_preferences(self):
        '''
        opens the preferences widget
        '''

        self.isEditor = False

        self.hide_all()
        self.mainWindow.bDock.use_preferences_mode()
        self.mainWindow.preferences.show()
        self.mainWindow.preferences.showMaximized()     


    def move_to_subprocess(self):
        '''
        adds subprocess specific buttons
        '''

        self.move_to_editor()
        self.mainWindow.ensure_tab_is_current()
        currentIdx = self.mainWindow.controller.currentFileIndex
        textScreen = self.mainWindow.controller.editorList[currentIdx].textScreen
        if textScreen.showMessages == False:
            textScreen.toggle_message_btn()

        self.mainWindow.bDock.use_subprocess_mode()
        
    def move_to_sphinx_preferences(self):
        '''
        opens the sphinx logger gui
        '''

        self.isEditor = False

        # determine the sphinx log path
        self.mainWindow.ensure_tab_is_current()
        fileIndex = self.mainWindow.controller.currentFileIndex
        fileName = self.mainWindow.controller.fileNameList[fileIndex]
        filePath = self.mainWindow.controller.filePathList[fileIndex]
      
        if fileName == None:
            self.mainWindow.display_info("Load or create a new project to begin")
            return
        if not re.search("\.rst",fileName,flags=re.IGNORECASE):
            self.mainWindow.display_info("%s\n\nis not a valid rst file so there are no Sphinx preferences"%(fileName))
            return

        sphinxLogPath = os.path.join(os.path.join(os.path.split(filePath)[0],"_sphinx"),'sphinx.log')
    
        if os.path.exists(sphinxLogPath) == False:
            self.mainWindow.display_warning("The sphinx preference log does not exist yet -- try building first.")
            return

        self.hide_all()
        sphinxLog = SphinxLogger(sphinxLogPath)
        if self.mainWindow.sphinxLogs.has_key(sphinxLogPath) == False:
            self.mainWindow.sphinxLogs[sphinxLogPath] = SphinxLoggerUI(sphinxLog,mainWindow=self.mainWindow)
            self.mainWindow.workspace.addWindow(self.mainWindow.sphinxLogs[sphinxLogPath])
            #self.mainWindow.hboxCenter.addWidget(self.mainWindow.sphinxLogs[sphinxLogPath])

        self.mainWindow.bDock.use_sphinx_log_mode()
        self.mainWindow.sphinxLogs[sphinxLogPath].show()
        self.mainWindow.sphinxLogs[sphinxLogPath].showMaximized()

    def move_to_new_project(self):
        '''
        opens the new project window
        '''

        self.isEditor = False

        self.hide_all()
        self.mainWindow.bDock.use_new_project_mode()
        self.mainWindow.newProject.show()
        self.mainWindow.newProject.showMaximized()

    def load_project_files(self):
        """
        gets all project files and loads them into the editor
        """
        
        self.move_to_editor()
        self.mainWindow.ensure_tab_is_current()

        fileIndex = self.mainWindow.controller.currentFileIndex
        filePath = self.mainWindow.controller.filePathList[fileIndex]
        fileName = self.mainWindow.controller.fileNameList[fileIndex]
        fileLang = self.mainWindow.controller.fileLangList[fileIndex]

        fileDir = os.path.split(filePath)[0]
        filesInProject = []
        
        self.start_waiting()
        for _file in os.listdir(fileDir):
            if re.search("\~|#",_file):
                continue

            if re.search("\.rst",fileName,flags=re.IGNORECASE) and re.search("\.rst",_file,flags=re.IGNORECASE):        
                filesInProject.append(os.path.join(fileDir,_file))
            if re.search("\.nw|\.rnw",fileName,flags=re.IGNORECASE) and re.search("\.nw|\.rnw",_file,flags=re.IGNORECASE):        
                filesInProject.append(os.path.join(fileDir,_file))

        for targetFile in filesInProject:
            if self.mainWindow.controller.filePathList.__contains__(targetFile):
                continue
            
            self.add_new_editor_tab(targetFile,fileLang=fileLang)
        self.stop_waiting()

        return filesInProject

    def build_all(self):
        '''
        builds all files open in the editor
        '''

        print "building all"

        numActive = self.mainWindow.controller.get_number_active_files()
        if numActive == 0:
            self.move_to_logo()
            return
        
        fileIndex = self.mainWindow.controller.currentFileIndex
        filePath = self.mainWindow.controller.filePathList[fileIndex]
        fileName = self.mainWindow.controller.fileNameList[fileIndex]
        fileLang = self.mainWindow.controller.fileLangList[fileIndex]
        
        filesToBuild = []
        for _file in self.mainWindow.controller.filePathList:
            if _file != None:
                filesToBuild.append(_file)
        
        ## if gui display ask user to continue
        if self.mainWindow != None:
            filesStr = re.sub("\[|\]|\s+","",str([os.path.split(_f)[-1] for _f in filesToBuild]))
            filesStr = "<p>"+ re.sub(",","<p>",filesStr) + "<p>"
            reply = QtGui.QMessageBox.question(self.mainWindow, self.mainWindow.controller.appName,
                                               "The following files will be compiled %s\nDo you want to continue?"%(filesStr),
                                               QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return 

        for tab in range(numActive):
            self.mainWindow.tabWidget.setCurrentIndex(tab)
            self.mainWindow.controller.currentFileIndex = tab
            fileName = self.mainWindow.controller.fileNameList[tab]

            filePath = self.mainWindow.controller.filePathList[tab]
            fileLang = self.mainWindow.controller.fileLangList[tab]
            goFlag = self.mainWindow.nga.build()
            
            if goFlag == False:
                break

            ## return to original tab
            self.mainWindow.tabWidget.setCurrentIndex(fileIndex)
            self.mainWindow.controller.currentFileIndex = fileIndex

    def view_output(self):
        """
        The ouput for code embedded in a document is written to a file 
        before it is integrated into the report.  This function views 
        the output file for the embedded code.
        """

        if self.mainWindow == None:
            return
        
        self.mainWindow.ensure_tab_is_current()
        currentIdx = self.mainWindow.controller.currentFileIndex
        filePath = self.mainWindow.controller.filePathList[currentIdx]
        lang = self.mainWindow.controller.fileLangList[currentIdx]
        lang = lang.lower()
        filePathBase = os.path.split(filePath)[0]
        dirPath = self.mainWindow.controller.ensure_dir_present(filePath)

        if lang == 'python':
            outFilePath = os.path.join(dirPath,"outPy.txt")
        if lang == 'r':
            outFilePath = os.path.join(dirPath,"outR.txt")

        self.mainWindow.dv = DocumentViewer(outFilePath,mainWindow=self.mainWindow)
        self.mainWindow.dv.show()
