#!/usr/bin/env python

'''
The controller class

A.Richards

'''

import re,os,csv,sys,time,re,shutil
import subprocess, threading
from PyQt4 import QtGui
from Logging import Logger
from version import __version__
from basedir import __basedir__

class Controller:
    def __init__(self,debug=False):
        '''
        construct an instance of the controller class
        to use invoke the method initialize
        '''

        ## basic application wide variables 
        self.appName = "lpEdit"
        self.debug = debug
        self.maxDocuments = 16
        self.version = __version__
        self.baseDir = __basedir__

        if self.debug == True:
            self.verbose = True
        else:
            self.verbose = False
        
        ## initialize 
        self.reset_all()

    def reset_all(self):
        """
        reset all variables and the layout
        """

        self.log = Logger()
        self.currentFileIndex = 0
        self.fileNameList = [None for i in range(self.maxDocuments)]
        self.filePathList = [None for i in range(self.maxDocuments)]
        self.fileLangList = [None for i in range(self.maxDocuments)]
        self.editorList = [None for i in range(16)]
        self.background = []

    def load_file(self,filePath,verbose=True,fileLang=None):
        '''
        takes a file path and loads the file into lpEdit
        '''

        ## ensure we have absolute file path
        if filePath != None:
            filePath = os.path.realpath(filePath)

        if os.path.exists(filePath) == False:
            print "WARNING: controller.load_file -- bad file path specified"

        ## check to see if already loaded
        fileName = os.path.split(filePath)[-1]
        if fileName in self.fileNameList:
            if verbose == True:
                print "WARNING: file of same name already loaded -- aborting load"
            return False

        numActive = self.get_number_active_files()
        if numActive >= self.maxDocuments:
            if verbose == True:
                print "WARNING: too many files already open -- aborting load"
    
        self.currentFileIndex = numActive
        self.filePathList[self.currentFileIndex] = filePath
        self.fileNameList[self.currentFileIndex] = fileName
        if fileLang != None:
            self.fileLangList[self.currentFileIndex] = fileLang
        elif re.search("\.Rnw|\.rnw",fileName):
            self.fileLangList[self.currentFileIndex] = 'R'
        else:
            self.fileLangList[self.currentFileIndex] = 'Python'

        return True

    def remove_file(self,fileName):
        '''
        removes a file from the list of loaded files'
        '''

        if fileName not in self.fileNameList:
            print "ERROR: Controller cannot remove file that is not present -- ignoring"
            return

        ## variables to change
        fileToRemoveIndex = self.fileNameList.index(fileName)
        fileName = self.fileNameList[fileToRemoveIndex]
        filePath = self.filePathList[fileToRemoveIndex]
        editor = self.editorList[fileToRemoveIndex]

        ## close the editor
        if editor != None:
            editor.close()

        self.fileNameList.remove(fileName)
        self.filePathList.remove(filePath)
        self.editorList.pop(fileToRemoveIndex)
        self.fileLangList.pop(fileToRemoveIndex)
        self.fileNameList = self.fileNameList + [None]
        self.filePathList = self.filePathList + [None]
        self.editorList = self.editorList + [None]
        self.fileLangList = self.fileLangList + [None]
        
    def clean_file(self,filePath):
        '''
        function to be used with unittests to ensure examples are working
        may also be used to ensure a new project
        '''

        filePathBase = os.path.split(filePath)[0]
        fileName = os.path.split(filePath)[-1]
        pdfFilePath = re.sub("\.rnw|\.nw|.rst",".pdf",filePath,flags=re.IGNORECASE)
        if re.search("\.rnw|\.nw",fileName,flags=re.IGNORECASE):
            dirName = "_latex"
        else:
            dirName = "_sphinx"
        dirPath = os.path.join(filePathBase,dirName)

        if os.path.isdir(dirPath) == False:
            return
        
        ## remove pdf file if present
        if os.path.exists(pdfFilePath):
            os.remove(pdfFilePath)

        ## remove all files in lp generated dir
        if os.path.isdir(dirPath):
            shutil.rmtree(dirPath)

    def save(self):
        '''
        saves changes to the log file
        '''

        self.log.write()

    def get_python_path(self,mainWindow=None):
        '''
        attempts to find the python path based on the system path and by searching
        '''

        if self.log.log['python_path'] != None:
            pythonPath = self.log.log['python_path']

            if os.path.exists(pythonPath) == False:
                msg = "ERROR: Controller -- given python path does not exist -- using default"
                if mainWindow != None:
                    mainWindow.display_info(msg)
                print msg
            else:
                return pythonPath


        cmdsToTry = ['python','python2.8','python2.7','python2.6'] 
        for cmd in cmdsToTry:
            pythonPath = self.find_command_path(cmd)
            if pythonPath != None and os.path.exists(pythonPath):
                return pythonPath
        
        return None

    def find_command_path(self,cmd):
        """
        used to search for a given command on a multiple operating systems
        """
        
        ## try to see if cmd is in the system path
        cmdPath = None
        try:
            if sys.platform == 'win32':
                p = os.popen('where %s'%cmd)
            else:
                p = os.popen('which %s'%cmd)
            cmdPath = p.readline()
            cmdPath = cmdPath[:-1]
        except:
            cmdPath = None

        if cmdPath != None and os.path.exists(cmdPath):
            return cmdPath

        ## look for cmd in several commonly installed places
        if sys.platform == 'win32':
            pathsToTry = []
            if cmd == 'python':
                pathsToTry = ["C:\Python28\python.exe",
                              "C:\Python27\python.exe",
                              "C:\Python26\python.exe"]
        elif sys.platform == 'darwin':
            pathsToTry = [os.path.join("/","usr","bin",cmd),
                          os.path.join("/","usr","local","bin",cmd),
                          os.path.join("/","opt","local","bin",cmd)]
        else:
            pathsToTry = [os.path.join("/","usr","bin",cmd),
                          os.path.join("/","usr","local","bin",cmd)]
            
        for cmdPath in pathsToTry:
            if cmdPath != None and os.path.exists(cmdPath) == True:
                return cmdPath

        return None

    def get_sphinx_path(self,mainWindow=None):
        """
        attempts to find the sphinx (sphinx-build) path based on the system path and by searching
        """
        
        if self.log.log['sphinx_path'] != None:
            sphinxPath = self.log.log['sphinx_path']

            if os.path.exists(sphinxPath) == False:
                msg = "ERROR: Controller -- given sphinx path does not exist -- using default"
                if mainWindow != None:
                    mainWindow.display_info(msg)
                print msg
            else:
                return sphinxPath
        cmdsToTry = ['sphinx-build','sphinx-build-2.8','sphinx-build-2.7','sphinx-build-2.6'] 
        for cmd in cmdsToTry:
            sphinxPath = self.find_command_path(cmd)
            if sphinxPath != None and os.path.exists(sphinxPath):
                return sphinxPath
        
        return None

    def get_latex_path(self,mainWindow=None):
        '''
        returns the latex path based on the system path or a provided one
        '''

        if self.log.log['latex_path'] != None:
            latexPath = self.log.log['latex_path']

            if os.path.exists(latexPath) == False:
                msg = "ERROR: Controller -- given latex path does not exist -- using default"
                if mainWindow != None:
                    mainWindow.display_info(msg)
                print msg
            else:
                return latexPath

        cmdsToTry = ['pdflatex'] 
        for cmd in cmdsToTry:
            latexPath = self.find_command_path(cmd)
            if latexPath != None and os.path.exists(latexPath):
                return latexPath
        
        return None

    def find_r_path_windows(self):
        dirsToTry = ["C:/Program Files/R","C:/Program Files (x86)/R"]
        r_path = None
        for rbaseDir in dirsToTry:
            if os.path.isdir(rbaseDir) == False:
                continue
            installedInstances = os.listdir(rbaseDir)
            if len(installedInstances) > 0:
                installedInstances.sort()
                rdir = installedInstances[-1]
                r_path = os.path.join(rbaseDir,rdir,"bin","R.exe")
                break
            
        return r_path


    def get_latex2html_path(self):
        """
        returns the path of the specified program to convert latex to html
        """

        if self.log.log['latex2html_path'] != None:
            rPath = self.log.log['latex2html_path']
        
        if sys.platform == 'win32':
            pthsToTry = ["C:/Program Files/latex2html.exe",
                         "C:/Program Files (x86)/latex2html.exe",
                         "C:/Program Files/tth.exe",
                         "C:/Program Files (x86)/tth.exe"]
        else:
            pthsToTry = ["/usr/bin/latex2html",
                         "/usr/local/bin/latex2html",
                         "/opt/local/bin/latex2html",
                         "/usr/bin/tth",
                         "/usr/local/bin/tth",
                         "/opt/local/bin/tth"]

        latex2html_path = None
        for pth in pthsToTry:
            if os.path.exists(pth) == True:
                latex2html_path = pth
                break
        return latex2html_path

    def get_r_path(self,mainWindow=None):
        '''
        returns the r path based on the system path or a provided one
        '''

        if self.log.log['r_path'] != None:
            rPath = self.log.log['r_path']

            if os.path.exists(rPath) == False:
                msg =  "ERROR: Controller -- given R path does not exist -- Please install R or specify a new path"
                if mainWindow != None:
                    mainWindow.display_info(msg)
                print msg
            else:
                return rPath

        ## windows
        if sys.platform == 'win32':
            rPath = self.find_r_path_windows()
            return rPath

        cmdsToTry = ['R'] 
        for cmd in cmdsToTry:
            rPath = self.find_command_path(cmd)
            if rPath != None and os.path.exists(rPath):
                return rPath

        return None
        
    def find_adobe_path_windows(self):
        dirsToTry = ["C:/Program Files/Adobe","C:/Program Files (x86)/Adobe"]
        adobe_path = None
        for abaseDir in dirsToTry:
            if os.path.isdir(abaseDir) == False:
                continue
            installedInstances = os.listdir(abaseDir)
            if len(installedInstances) > 0:
                installedInstances.sort()
                adir = installedInstances[-1]
                adobe_path = os.path.join(abaseDir,adir,"Reader","AcroRd32.exe")
                break
            
        return adobe_path

    def get_pdfviewer_path(self,mainWindow=None):
        '''
        finds the pdfviewer path (on windows it looks for adobe)
        '''
        
        if self.log.log['pdfviewer_path'] != None:
            pdfviewerPath = self.log.log['pdfviewer_path']
            
            ## exceptions
            if pdfviewerPath == 'open' and sys.platform == 'darwin':
                return pdfviewerPath

            if os.path.exists(pdfviewerPath) == False:
                msg =  "ERROR: the pdfviewer path does not exist -- using default"
                if mainWindow != None:
                    mainWindow.display_info(msg)
                print msg
            else:
                return pdfviewerPath

        if sys.platform == 'win32':
            return self.find_adobe_path_windows()
        elif sys.platform == 'darwin':
            return "open"
        
        cmdsToTry = ['okular','evince','acroread'] 
        for cmd in cmdsToTry:
            pdfviewerPath = self.find_command_path(cmd)
            if pdfviewerPath != None and os.path.exists(pdfviewerPath):
                return pdfviewerPath

        return None
                
    def ensure_dir_present(self,filePath):
        '''
        given a file path create a dir next to the Rnw or otherwise valid file
        '''

        filePathBase = os.path.split(filePath)[0]
        fileName = os.path.split(filePath)[-1]
        if re.search("\.rnw|\.nw",fileName,flags=re.IGNORECASE):
            lpDirName = "_latex"
        elif re.search("\.rst",fileName,flags=re.IGNORECASE):
            lpDirName = "_sphinx"
        lpDirPath = os.path.join(filePathBase,lpDirName)
        
        ## create the directory if necessary
        if os.path.isdir(lpDirPath) == False:
            os.mkdir(lpDirPath)

        return lpDirPath

    def get_number_active_files(self):
        '''
        returns the number of active files
        '''

        totalActive = 0
        for fileName in self.fileNameList:
            if fileName != None:
                totalActive += 1

        return totalActive

    def sanitize_check(self,script):
        """
        standard function to sanitize file name inputs
        """

        if re.search(">|<|\*|\||^\$|;|#|\@|\&",script):
            return False
        else:
            return True

    def get_templates_dir(self):
        templatesDir = os.path.realpath(os.path.join(self.baseDir,'templates'))
        return templatesDir

    def get_styfiles_dir(self):
        styfilesDir = os.path.realpath(os.path.join(self.baseDir,'styfiles'))
        return styfilesDir

    def get_sphinx_files_dir(self):
        sphinxfilesDir = os.path.realpath(os.path.join(self.baseDir,'sphinxfiles'))
        return sphinxfilesDir

    def initialize_sphinx_project(self,dirPath,filePath):
        """
        the dirPath is the path where the rst project resides
        Use existing *.rst and conf.py files
        If necessary create index.rst and conf.py
        """

        ## variables
        sphinxDir = self.get_sphinx_files_dir()
        filePathBase,fileName = os.path.split(filePath)

        ## check to see if index.rst and conf.py need to be created
        for fName in ["conf.py"]:
            fPath = os.path.join(dirPath,fName)
            if os.path.exists(fPath) == False:
                shutil.copy(os.path.join(sphinxDir,fName),fPath)

        createIndex = False
        for fName in ["index.rst"]:
            fPath = os.path.join(dirPath,fName)
            if os.path.exists(fPath) == False:
                createIndex = True
            
        ## create the _build and _source dirs if necessary
        for dirName in ["_build", "_source","_static",]:
            if os.path.isdir(os.path.join(dirPath,dirName)) == False:
                os.mkdir(os.path.join(dirPath,dirName))

        ## move all source files into target dir unless already present 
        rstFilesList = []
        for fName in os.listdir(filePathBase):
            if re.search("\.rst",fName,flags=re.IGNORECASE):
                if re.search("\~$",fName):
                    continue

                rstFilesList.append(fName)

        ## copy project files that are not alread present
        for rstFile in rstFilesList:
            sourceFilePath = os.path.join(filePathBase,rstFile)
            targetFilePath = os.path.join(dirPath,rstFile)
            if os.path.exists(targetFilePath) == False:
                shutil.copy(sourceFilePath,targetFilePath)

        ## add to any newly created index.rst if one does not exist
        if createIndex == True:
            indexFilePath = os.path.join(filePathBase,'index.rst')
            fid = open(indexFilePath,'w')
            fid.write(".. master file, created automatically by lpEdit\n")
            fid.write("\nContents\n=========================\n\n")
            fid.write(".. toctree::\n   :maxdepth: 1\n\n")
            for rstFile in rstFilesList:
                if rstFile == 'index.rst':
                    continue
                fid.write("   %s\n"%re.sub("\.rst","",rstFile,flags=re.IGNORECASE))
            fid.close()
            shutil.copy(indexFilePath,os.path.join(dirPath,'index.rst'))

    def language_quickcheck(self,chunksFilePath,fileLanguage):
        """
        look into the extracted code and see if there are obvious
        signs that the language selected is incorrect
        """
        
        ## variables
        pythonSpecific = ["import","from"]
        rSpecific = ["<-"]
        fileLanguage = fileLanguage.lower()

        if os.path.exists(chunksFilePath) == False:
            return

        fid = open(chunksFilePath,'r')
        isValid = True
        for linja in fid:
            if fileLanguage == 'python':
                for kw in rSpecific:
                    if re.search(kw,linja):
                        isValid = False
            if fileLanguage == 'r':
                for kw in pythonSpecific:
                    if re.search(kw,linja):
                        isValid = False
        fid.close()

        return isValid
