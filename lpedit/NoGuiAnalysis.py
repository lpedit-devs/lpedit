#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os,sys,re,shutil,time
import webbrowser,threading
from RunSubprocess import RunSubprocess
from SphinxLogger import SphinxLogger
from Logging import Logger
from Controller import Controller


class NoGuiAnalysis():

    def __init__(self,controller=None,mainWindow=None):
      
        ## input variables
        if controller == None:
            self.controller = Controller()
        else:
            self.controller = controller
        self.mainWindow = mainWindow
        self.validLanguages = ['r','python']
        self.sphinxLog = None
        self.goFlag = False
        self.reload_program_paths()
        
    def reload_program_paths(self):
        """
        function to update the paths to programs for system calls
        """
        
        ## ensure that the log file is loaded
        if len(self.controller.log.log.items()) < 1:
           self.controller.log = Logger() 

        self.rPath = self.controller.get_r_path(mainWindow=self.mainWindow)
        self.pythonPath = self.controller.get_python_path(mainWindow=self.mainWindow)
        self.sphinxPath = self.controller.get_sphinx_path(mainWindow=self.mainWindow)
        self.latexPath = self.controller.get_latex_path()
        self.parsePath = os.path.join(self.controller.baseDir,"ParseEmbedded.py")
        self.latex2htmlPath = self.controller.get_latex2html_path()

    def build(self,fileName=None,verbose=False):
        """
        generic command to build a rst,nw or rnw document
        """

        ## variables
        self.goFlag = False
        if self.mainWindow != None:
            self.mainWindow.ensure_tab_is_current()
        
        ## if a fileName is specified the set the current index
        if fileName != None and fileName in self.controller.fileNameList:
            currentIdx = self.controller.fileNameList.index(fileName)
            self.controller.currentFileIndex = currentIdx
        
        currentIdx = self.controller.currentFileIndex
        fileName = self.controller.fileNameList[currentIdx]
        filePath = self.controller.filePathList[currentIdx]

        fileLanguage = self.controller.fileLangList[currentIdx]
        self.reload_program_paths()
        goFlag = None

        if self.mainWindow != None:
            editor = self.mainWindow.controller.editorList[currentIdx] 
            editor.clear_messages()
        
        self.output_text("BUILDING... %s"%fileName)

        ## error checking
        isClean = self.controller.sanitize_check(filePath)
        if isClean == False:
            msg = "Invalid file/dir name\n"
            msg += "%s\nremove characters like '$','#' and '&' then try again"%(filePath) 
            self.display_error(msg)
            return

        isActive = self.is_active_project(filePath)
        if not isActive:
            return
        isTemplate = self.is_template()
        if isTemplate == True:
            return

        fileLanguage = fileLanguage.lower()
        if fileLanguage not in self.validLanguages:
            msg = "Valid languages are %s not %s"%(self.validLanguages,fileLanguage)
            self.display_error(msg)
            return

        ## save file
        if self.mainWindow != None:
            self.mainWindow.file_save(display=False)

        ## run the appropriate builder
        if re.search("\.rst",fileName,flags=re.IGNORECASE):
            self.build_rst(verbose=verbose)
        elif re.search("\.rnw|\.nw",fileName,flags=re.IGNORECASE):
            self.build_nw(verbose=verbose)
        else:
            msg = "Invalid file name extension\n"
            msg +="...lpEdit cannot build\n"
            msg +=filePath
            self.display_error(msg)

    def load_file(self,filePath,fileLang=None):
        '''
        use the controller to load a specified file
        '''

        filePath = os.path.realpath(filePath)

        if not os.path.exists(filePath):
            print("ERROR: invalid file path specified for load")
            print("... %s"%filePath)
            return
        
        isValid = self.controller.load_file(filePath,fileLang=fileLang)
        if isValid == False:
            print "ERROR: controller could not load specified file"
            print "\t", filePath

    def clean_file(self,filePath,verbose=False):
        '''
        cleans a directory of its files -- function used with unittests
        '''
        
        self.controller.clean_file(filePath)

    def output_text(self,txt):
        currentIdx = self.controller.currentFileIndex
        
        if self.mainWindow != None:
            if self.mainWindow.controller.editorList[currentIdx].textScreen.showMessages == False:
                self.mainWindow.controller.editorList[currentIdx].textScreen.toggle_message_btn()
            self.mainWindow.controller.editorList[currentIdx].textScreen.add_text(txt)
        else:
            print txt

    def copy_included_files(self,filePath,dirPath):
        """
        Copy files that are included with the keyword INCLUDE
        The source file path is given and it is scanned for INCLUDE
        Each include may be multiple file paths (comma delim)
        """
        
        baseDir = os.path.split(filePath)[0]
        
        ## adjust for subdirectories
        if os.path.split(baseDir)[1] != os.path.split(os.path.split(dirPath)[0])[1]:
            subdir = os.path.split(baseDir)[1]
            targetDir = os.path.join(dirPath,subdir)
        else:
            targetDir = dirPath
            subdir = None

        fid = open(filePath,'r')
        includedFiles = []
        found = False
        for linja in fid:
            if re.search("^%|^\.\. ",linja) and re.search("INCLUDE",linja):
                linja = re.sub("INCLUDE[\W|\w]","",linja)
                linja = re.sub("\%|\s+|^\.\.","",linja)
                found = True
                linja = re.split(",",linja)
                for includedFile in linja:
                    if os.path.exists(includedFile):
                        includedFiles.append(os.path.realpath(includedFile))
                    else:
                        includedFilePath = os.path.join(baseDir,includedFile)
                        includedFiles.append(os.path.realpath(includedFilePath))

        for includedFilePath in includedFiles:
            includedFilePath = includedFilePath
            includedFileName = os.path.split(includedFilePath)[-1]
            includedFileDir = os.path.split(includedFilePath)[-1]
            newFilePath = os.path.join(targetDir,includedFileName)

            if not os.path.exists(includedFilePath):
                msg = "Invalid INCLUDE path...\n"         
                msg += includedFilePath
                if self.mainWindow != None:
                    self.mainWindow.display_warning(msg)
                else:
                    print msg
                return False

            if os.path.islink(newFilePath):
                os.remove(newFilePath)
            if os.path.exists(newFilePath):
                os.remove(newFilePath)

            self.output_text("INCLUDE: %s \n...%s"%(includedFilePath,newFilePath))

            os.symlink(includedFilePath,newFilePath)

        return True

    def is_active_project(self,currentFilePath):
        """
        check for an active project
        """
        if currentFilePath == '' or currentFilePath == None:
            msg = "Load or create a new file before compiling code"
            self.display_error(msg)
            return False

        return True

    def is_template(self):
        """
        checks to see if currentFile is a template or not
        """
        templatesDir = self.controller.get_templates_dir()
        currentFilePath = self.controller.filePathList[self.controller.currentFileIndex]
        currentFileName = self.controller.fileNameList[self.controller.currentFileIndex]

        if os.path.join(templatesDir,currentFileName) == currentFilePath:
            msg = "Use 'Save As' before trying to work with template"
            self.display_error(msg)
            return True

        return False

    def display_error(self,msg):
        """
        generic function to display an error
        """
        if self.mainWindow != None:
            self.mainWindow.display_warning(re.sub("\n","<p>",msg))
        else:
            print "ERROR: ", msg

    def build_nw(self,verbose=True):
        """
        uses system calls to compile nw or sweave code
        """

        ## variables
        templatesDir = self.controller.get_templates_dir()
        currentIdx = self.controller.currentFileIndex
        filePath = self.controller.filePathList[currentIdx]
        fileName = self.controller.fileNameList[currentIdx] 
        fileLanguage = self.controller.fileLangList[currentIdx]
        fileLanguage = fileLanguage.lower()
        filePathBase = os.path.split(filePath)[0]
        texFileName = re.sub("\.rnw|\.nw|\.rst",".tex",fileName,flags=re.IGNORECASE)
        dirPath = self.controller.ensure_dir_present(filePath)
        assemblePath = os.path.join(self.controller.baseDir,"AssembleOutNW.py")

        ## ensure we are using the correct builder
        if not re.search("\.nw|\.rnw",fileName,flags=re.IGNORECASE):
            msg = "NoGuiAnalysis: Incorrect builder -- skipping"
            self.display_error(msg)
            return

        ## ensure the correct builder is being used (based on extension)
        if re.search("\.rnw",fileName,flags=re.IGNORECASE) and fileLanguage != 'r':
            msg = "Sweave styled documents cannot contain code\n"
            msg += "other than R. \nSave the document as a *.nw file and try again"
            self.display_error(msg)
            return
        elif re.search("\.rnw",fileName,flags=re.IGNORECASE):
            builder = 'sweave'
        else:
            builder = 'nw'
        
        ## copy target file to dir
        targetFilePath = os.path.join(dirPath,fileName)
        shutil.copy(filePath,targetFilePath)

        ## copy included files
        goFlag = self.copy_included_files(filePath,dirPath)
        if goFlag == False:
            errMsg = "Build aborted"
            self.display_error(errMsg)
            return False
 
        ## move a copy of each sty file into the dir
        styfilesDir = self.controller.get_styfiles_dir()
        for styfile in os.listdir(styfilesDir):
            if not re.search("\.sty",styfile):
                continue
            if os.path.exists(os.path.join(dirPath,styfile)) == False:
                shutil.copy(os.path.join(styfilesDir,styfile),os.path.join(dirPath,styfile))

        ## paths
        if fileLanguage == 'python':
            chunksFilePath = os.path.join(dirPath,"chunks.py")
            outFilePath = os.path.join(dirPath,"outPy.txt")
            langCmd = self.pythonPath
        elif fileLanguage == 'r':
            chunksFilePath = os.path.join(dirPath,"chunks.R")
            outFilePath = os.path.join(dirPath,"outR.txt")
            langCmd = self.rPath+'script'

        ## remove old versions of the files
        for fname in [chunksFilePath,outFilePath,os.path.join(dirPath,texFileName)]:
            if os.path.exists(fname):
                os.remove(fname)

        if builder == 'sweave':
            self.output_text('BUILDING WITH SWEAVE...')
            compileCmd = '"%s" CMD Sweave "%s"'%(self.rPath,targetFilePath)
            self.run_subprocess(compileCmd)

            ## move the output to build directory
            tmpTex = os.path.join(os.getcwd(),texFileName)
            if os.path.exists(tmpTex):
                shutil.move(tmpTex,os.path.join(dirPath,texFileName))

        elif builder == 'nw':
            ## extract the code
            self.output_text("EXTRACTING CODE...")
            compileCmd = '"%s" "%s" -i "%s" -o "%s"'%(self.pythonPath,self.parsePath,
                                                      targetFilePath,chunksFilePath)
            self.run_subprocess(compileCmd)
            
            ## run extracted code
            if os.path.exists(chunksFilePath):
                self.output_text("RUNNING CODE...")
                compileCmd = '"%s" "%s" > "%s"'%(langCmd,chunksFilePath,outFilePath)
                self.run_subprocess(compileCmd)
            else:
                self.output_text("EXITING EARLY... could not find extracted code")
                return False

            if self.mainWindow != None:
                self.mainWindow.transitions.update_ui()

            ## exit early on error
            goFlag = self.check_standard_error(self.stdErr)
            
            if goFlag == False:
                self.output_text("EXITING EARLY... ERROR found in embedded code")
                return False

            ## reassemble the *.tex file with code results
            if os.path.exists(outFilePath):
                self.output_text("REASSEMBLING CODE AND RESULTS...")
                compileCmd = '"%s" "%s" -i "%s" -o "%s"'%(self.pythonPath,assemblePath,
                                                          targetFilePath,outFilePath)
                self.run_subprocess(compileCmd)
            else:
                self.output_text("EXITING EARLY... there was a problem running the embedded code")
                return False
                
        ## check that we have a valid build
        self.goFlag = self.ensure_valid_build(os.path.join(dirPath,texFileName))

    def check_standard_error(self,stdErr):
        """
        a function that halts on certain standard error messages
        """

        if stdErr != None and re.search('Traceback|Error:|Exception occurred:',stdErr,flags=re.IGNORECASE):
            return False
        else:
            return True

    def build_rst(self,verbose=True):
        """
        uses system calls to compile a sphinx project
        """
        
        ## variables
        currentIdx = self.controller.currentFileIndex
        filePath = self.controller.filePathList[currentIdx]
        filePathBase = os.path.split(filePath)[0]
        fileName = self.controller.fileNameList[currentIdx]
        fileLanguage = self.controller.fileLangList[currentIdx]
        fileLanguage = fileLanguage.lower()
        filePathBase = os.path.split(filePath)[0]
        assemblePath = os.path.join(self.controller.baseDir,"AssembleOutRst.py")
        tmpFilePath = filePath + ".tmp"

        ## ensure we are using the correct builder
        if not re.search("\.rst",fileName,flags=re.IGNORECASE):
            msg = "NoGuiAnalysis: Incorrect builder -- skipping"
            self.display_error(msg)
            return

        ## copy included files
        dirPath = self.controller.ensure_dir_present(filePath)
        goFlag = self.copy_included_files(filePath,dirPath)
        if goFlag == False:
            errMsg = "Build aborted"
            self.display_error(errMsg)
            return

        ## move a copy of each sty file into the dir
        styfilesDir = self.controller.get_styfiles_dir()
        for styfile in os.listdir(styfilesDir):
            if not re.search("\.sty",styfile):
                continue
            if os.path.exists(os.path.join(dirPath,styfile)) == False:
                shutil.copy(os.path.join(styfilesDir,styfile),os.path.join(dirPath,styfile))

        ## initialize a sphinx project
        self.controller.initialize_sphinx_project(filePath)
        self.controller.copy_sphinx_files()
        self.sphinxLog = SphinxLogger(os.path.join(dirPath,'sphinx.log'))
        self.sphinxLog.write()

        ## ensure the current file is copied
        fileBase = os.path.split(filePath)[0]

        if fileBase != self.controller.sphinxProjectBase:
            subdirName = os.path.basename(os.path.dirname(filePath))
            targetFilePath = os.path.join(dirPath,subdirName,fileName)
        else:
            targetFilePath = os.path.join(dirPath,fileName)

        print 'copying...', targetFilePath

        shutil.copy(filePath,targetFilePath)

        ## compile
        if fileLanguage == 'python':
            chunksFilePath = os.path.join(dirPath,"chunks.py")
            outFilePath = os.path.join(dirPath,"outPy.txt")
            langCmd = self.pythonPath
        elif fileLanguage == 'r':
            chunksFilePath = os.path.join(dirPath,"chunks.R")
            outFilePath = os.path.join(dirPath,"outR.txt")
            langCmd = self.rPath+'script'

        ## remove old versions of files
        for fname in [chunksFilePath,outFilePath,tmpFilePath]:
            if os.path.exists(fname):
                os.remove(fname)

        ## extract the code from the file
        self.output_text("EXTRACTING CODE...")
        compileCmd = '"%s" "%s" -i "%s" -o "%s"'%(self.pythonPath,self.parsePath,
                                                  filePath,chunksFilePath)
        self.run_subprocess(compileCmd)

        ## run the embedded code
        if os.path.exists(chunksFilePath):
            self.output_text("RUNNING CODE (%s)..."%(fileLanguage))
            compileCmd = '"%s" "%s" > "%s"'%(langCmd,chunksFilePath,outFilePath)
            self.run_subprocess(compileCmd)
        else:
            self.output_text("EXITING EARLY... could not find extracted code")
            return False

        ## exit early on error
        goFlag = self.check_standard_error(self.stdErr)
        if goFlag == False:
            self.output_text("EXITING EARLY... ERROR found in embedded code")
            return False

        ## reassemble the *.rst file with code results
        if os.path.exists(outFilePath):
            self.output_text("\nREASSEMBLING CODE AND RESULTS...")   
            compileCmd = '"%s" "%s" -i "%s" -o "%s" -l %s'%(self.pythonPath,
                                                            assemblePath,
                                                            filePath,
                                                            outFilePath,
                                                            fileLanguage)
            self.run_subprocess(compileCmd)
        else:
            self.output_text("EXITING EARLY... there was a problem running the embedded code")
            return False
        
        ## overwrite the old rst file
        if os.path.exists(tmpFilePath):
            shutil.move(tmpFilePath,targetFilePath)
            self.goFlag = True
            self.output_text("BUILD COMPLETED SUCCESFULLY.")
            if self.mainWindow != None:
                editor = self.mainWindow.controller.editorList[currentIdx] 
                if editor.textScreen.showMessages == True:
                    editor.textScreen.toggle_message_btn()
            return True


    def show_error(self):
        """
        show error in messages
        """

        currentIdx = self.controller.currentFileIndex
        if self.mainWindow != None:
            self.mainWindow.display_info("Build did not complete correctly")
            editor = self.mainWindow.controller.editorList[currentIdx] 
            if editor.textScreen.showMessages == False:
                editor.textScreen.toggle_message_btn()
        else:
            print "WARNING: Build did not complete correctly"
        return
       
    def ensure_valid_build(self,texFilePath):
        """
        ensure build completed correctly
        """

        currentIdx = self.controller.currentFileIndex
        if not os.path.exists(texFilePath):
            self.show_error()
            return False
        else:
            self.output_text("BUILD COMPLETED SUCCESFULLY.")
            if self.mainWindow != None:
                editor = self.mainWindow.controller.editorList[currentIdx] 
                if editor.textScreen.showMessages == True:
                    editor.textScreen.toggle_message_btn()
            return True

    def on_subprocess_complete(self):
        """
        on completion of a subprocess return to editor mode
        """

        if self.mainWindow != None:
            self.mainWindow.transitions.move_to_editor()

        ## debugging
        #print 'output',self.stdOut,self.stdErr

    def run_subprocess(self,cmd,background=False,clear=True):
        self.stdErr, self.stdOut = None, None

        ## create a thread to check status of subprocess
        def target(process,nga):
            while process.thread.is_alive():
                currentIdx = nga.controller.currentFileIndex

                if nga.mainWindow != None:
                    editor = nga.controller.editorList[currentIdx] 
                    editor.clear_messages()
      
                time.sleep(1)
                nga.output_text(process.cmd)
                stdOut = process.stdOut
                stdErr = process.stdErr
                if stdOut == None or len(stdOut) == 0:
                    stdOut = ''
                if stdErr == None or len(stdErr) == 0:
                    stdErr = ''

                if stdOut != '':
                    nga.output_text("\n"+stdOut)
                if stdErr != '':
                    ## ignore certain stderr
                    if re.search("\[2K\n",stdErr):
                        stdErr = ''
                        continue

                    nga.output_text("\n"+stdErr)

            self.stdErr, self.stdOut = stdErr, stdOut
            nga.on_subprocess_complete()

        ## move to appropriate mode
        if self.mainWindow != None:
            self.mainWindow.transitions.move_to_subprocess()
            self.mainWindow.process = RunSubprocess(cmd)
            process = self.mainWindow.process
            self.mainWindow.transitions.update_ui()
        else:
            process = RunSubprocess(cmd)

        ## begin the threaded subprocess
        returnCode = process.run(timeout=None)

        ## run the process in the background
        if background == True:
            if self.mainWindow != None:
                self.mainWindow.transitions.move_to_editor()
            return True

        ## start a thread to check on process status
        if self.mainWindow != None:
            self.mainWindow.waitThread = threading.Thread(target=target(process,self))
            waitThread = self.mainWindow.waitThread
        else:
            waitThread = threading.Thread(target=target(process,self))

        waitThread.start()

    def compile_pdf(self,verbose=True,recompile=False):
        """
        uses system calls to compile the latex code to pdf
        """

        # variables
        if self.mainWindow != None:
            self.mainWindow.ensure_tab_is_current()

        currentIdx = self.controller.currentFileIndex
        filePath = self.controller.filePathList[currentIdx]
        filePathBase = os.path.split(filePath)[0]
        fileName = self.controller.fileNameList[currentIdx]

        ## error checking
        isActive = self.is_active_project(filePath)
        if not isActive:
            return
        isTemplate = self.is_template()
        if isTemplate == True:
            return

        ## clear the text
        if self.mainWindow != None:
            editor = self.mainWindow.controller.editorList[currentIdx] 
            editor.clear_messages()

        ## more variables
        dirPath = self.controller.ensure_dir_present(filePath)

        if re.search("\.rnw|\.nw",fileName,flags=re.IGNORECASE):
            texFileName = re.sub("\.rnw|\.nw",".tex",fileName,flags=re.IGNORECASE)
            texFilePath = os.path.join(dirPath,texFileName)
            pdfFileName = re.sub("\.rnw|\.nw",".pdf",fileName,flags=re.IGNORECASE)        
            pdfFileName = re.sub("\s+","_",pdfFileName)
            pdfFilePath = os.path.join(dirPath,pdfFileName)
            projectType = 'nw'
        else:
            sl = SphinxLogger(os.path.join(dirPath,'sphinx.log'))
            texFileName = sl.log['project_name'] + ".tex"
            texFilePath = os.path.join(dirPath,"_build",texFileName)
            pdfFileName = sl.log['project_name'] + ".pdf"
            pdfFileName = re.sub("\s+","_",pdfFileName)
            pdfFilePath = os.path.join(dirPath,"_build",pdfFileName)
            projectType = 'sphinx'

        ## if sphinx project
        if projectType == 'sphinx':
            self.output_text("BUILDING SPHINX (LaTeX)...")
            sl = SphinxLogger(os.path.join(dirPath,'sphinx.log'))
            texFileName = self.sphinxLog.log['project_name'] + ".tex"
            texFilePath = os.path.join(dirPath,"_build",texFileName)
        
            ## remove old versions of files
            for fname in [texFilePath]:
                if os.path.exists(fname):
                    os.remove(fname)
        
            compileCmd = "%s -b latex %s %s"%(self.sphinxPath,dirPath,os.path.join(dirPath,"_build"))
            self.run_subprocess(compileCmd)
            goFlag = self.ensure_valid_build(texFilePath)

            if goFlag == False:
                self.output_text("EXITING EARLY... Could not create tex file.")
                return False

        if not os.path.exists(texFilePath):
            errMsg = "'%s' does not exist\nDid you build the file successfully?"%(texFileName)
            self.display_error(errMsg)
            return

        ## compile
        ## with errors nonstopmode will do its best to compile, batchmode will supress pdf output
        if projectType == 'nw':
            texOut = dirPath
        else:
            texOut = os.path.join(dirPath,'_build')
        latexCompileCmd = '"%s" -interaction=nonstopmode -output-directory %s "%s"'%(self.latexPath,texOut,texFilePath)
 
        ## remove pdf files
        for fname in [pdfFilePath]:
            if os.path.exists(fname):
                os.remove(fname)
        
        ## first pass to match citations and refs
        self.run_subprocess(latexCompileCmd)
        goFlag = self.check_pdf_compile(pdfFilePath)
        if goFlag == False:
            return

        ## recompile if specified
        if recompile:
            self.run_subprocess(latexCompileCmd)

        ## check to see if there was a bib file
        bibFilePath = None
        fid = open(filePath,'r')
        for linja in fid:
            if re.search("\{.+\.bib\}",linja):
                match = re.findall("\{.+\.bib\}",linja)
                bibFileName = match[0][1:-1]
                bibFilePath = os.path.join(filePathBase,bibFileName)
        fid.close()

        ## if there was a bib
        if bibFilePath != None:
            cwd = os.getcwd()
            os.chdir(texOut)
            bibtexPath = re.sub('pdflatex','bibtex',self.latexPath)
            compileCmd = '"%s" "%s"'%(bibtexPath,texFileName[:-4])
            self.run_subprocess(compileCmd)
            os.chdir(cwd)

            ## compile twice for bib
            #if os.path.exists(pdfFilePath):
            self.run_subprocess(latexCompileCmd)
            #self.run_subprocess(latexCompileCmd)
                
        ## check to see that everything worked
        goFlag = self.check_pdf_compile(pdfFilePath)
        if goFlag == False:
            return

        ## move pdf into same directory as src file
        if os.path.exists(pdfFilePath) == False:
            print "ERROR: NoGuiAnalysis.compile_latex --- could not find pdfFileName to move"
            return

        shutil.move(pdfFilePath,os.path.join(filePathBase,pdfFileName))

    def compile_html(self,verbose=True):
        """
        use system calls to compile either latex to html or rst to html
        """

        # variables
        if self.mainWindow != None:
            self.mainWindow.ensure_tab_is_current()

        currentIdx = self.controller.currentFileIndex
        filePath = self.controller.filePathList[currentIdx]
        filePathBase = os.path.split(filePath)[0]
        fileName = self.controller.fileNameList[currentIdx]

        ## error checking
        isActive = self.is_active_project(filePath)
        if not isActive:
            return
        isTemplate = self.is_template()
        if isTemplate == True:
            return

        ## clear the text
        if self.mainWindow != None:
            editor = self.mainWindow.controller.editorList[currentIdx] 
            editor.clear_messages()

        ## more variables
        dirPath = self.controller.ensure_dir_present(filePath)
        
        ## determine the type of project 
        if re.search("\.rnw|\.nw",fileName,flags=re.IGNORECASE):
            projectType = 'latex'
        elif re.search("\.rst",fileName,flags=re.IGNORECASE):
            sl = SphinxLogger(os.path.join(dirPath,'sphinx.log'))
            projectType = 'sphinx'
        else:
            errMsg = "Invalid source file for compile_html -- skipping compile\n%s"%fileName
            self.display_error(errMsg)

        if projectType == 'sphinx':
            ## before building remove old html
            htmlFilePath =  os.path.join(dirPath,"_build","index.html")
            if os.path.exists(htmlFilePath):
                os.remove(htmlFilePath)

            ## use sphinx build to create the html document
            self.output_text("BUILDING WITH SPHINX (Sphinx)...")
            sl = SphinxLogger(os.path.join(dirPath,'sphinx.log'))
            
            compileCmd = "%s -b html %s %s"%(self.sphinxPath,dirPath,os.path.join(dirPath,"_build"))
            self.run_subprocess(compileCmd)
        else:
            htmlFileName =  re.sub("\.rnw|\.nw",".html",fileName,flags=re.IGNORECASE)
            htmlFilePath =  os.path.join(dirPath,htmlFileName)
            if os.path.exists(htmlFilePath):
                os.remove(htmlFilePath)

            ## use external program i.e. latex2html to create the html documents
            self.output_text("BUILDING HTML (LaTeX)...")
            sl = SphinxLogger(os.path.join(dirPath,'sphinx.log'))
            
            ## ensure we have valid program to build
            if self.latex2htmlPath == None:
                errMsg = "No program is specified for LaTeX to HTML conversion\nGo to Preferences"
                if self.mainWindow != None:
                    self.mainWindow.display_info(errMsg)
                else:
                    print errMsg
                return

            targetFilePath = os.path.join(dirPath,fileName)
            compileCmd = '"%s" "%s"'%(self.latex2htmlPath,targetFilePath)
            self.run_subprocess(compileCmd)

            ## point to main html file
            fileNameBase = re.sub("\.rnw|\.nw","",fileName,flags=re.IGNORECASE)
            htmlFilePath = os.path.join(dirPath,fileNameBase,'index.html')

        ## check that html  was created succesfully
        goFlag = self.check_standard_error(self.stdErr)
        
        if goFlag == False:
            self.output_text("EXITING EARLY... ERROR: html was not created succesfully")
            return False

        ## ensure html was created
        if os.path.exists(htmlFilePath) == False:        
            errMsg = "The HTML did not compile correctly \n%s"%htmlFilePath
            self.display_error(errMsg)
        else:
            if self.mainWindow != None:
                if self.controller.editorList[currentIdx].textScreen.showMessages == True:
                    self.controller.editorList[currentIdx].textScreen.toggle_message_btn()
            
    def check_pdf_compile(self,pdfFilePath):
        currentIdx = self.controller.currentFileIndex
        if not os.path.exists(pdfFilePath):
            errMsg = "LaTeX did not compile correctly"
            self.display_error(errMsg)

            if self.mainWindow != None:
                self.mainWindow.display_info(errMsg)
                if self.controller.editorList[currentIdx].textScreen.showMessages == False:
                    self.controller.editorList[currentIdx].textScreen.toggle_message_btn()
            else:
                print "ERROR: " + errMsg
            return False
        else:
            self.output_text("PDF CREATED SUCCESFULLY.")
            if self.mainWindow != None: 
                if self.controller.editorList[currentIdx].textScreen.showMessages == True:
                    self.controller.editorList[currentIdx].textScreen.toggle_message_btn()

            return True

    def view_pdf(self):
        '''
        uses system calls to view the pdf
        '''

        ## variables
        if self.mainWindow != None:
            self.mainWindow.ensure_tab_is_current()

        isTemplate = self.is_template()
        if isTemplate == True:
            return

        currentIdx = self.controller.currentFileIndex
        filePath = self.controller.filePathList[currentIdx]
        filePathBase = os.path.split(filePath)[0]
        fileName = self.controller.fileNameList[currentIdx]
        dirPath = self.controller.ensure_dir_present(filePath)
        
        ## error checking
        isActive = self.is_active_project(filePath)
        if not isActive:
            return

        ## clear the text
        if self.mainWindow != None:
            editor = self.mainWindow.controller.editorList[currentIdx] 
            editor.clear_messages()

        ## more variables 
        if re.search("\.rnw|\.nw",fileName,flags=re.IGNORECASE):
            pdfFileName = re.sub("\.rnw|\.nw",".pdf",fileName,flags=re.IGNORECASE)
        else:
            sl = SphinxLogger(os.path.join(dirPath,'sphinx.log'))
            pdfFileName = sl.log['project_name'] + ".pdf"
            
        pdfFilePath = os.path.join(filePathBase,pdfFileName)

        if not os.path.exists(pdfFilePath):
            errMsg = "'%s' does not exist\nDid you run the PDF compilation script?"%(pdfFilePath)
            self.display_error(errMsg)
            return

        pdfViewerPath = self.controller.get_pdfviewer_path()

        if pdfViewerPath == None:
            errMsg = "No pdf viewer found -- do you have one installed?"
            self.display_error(errMsg)
                
        ## view the pdf
        pdfViewerCmd = '"%s" "%s"'%(pdfViewerPath,pdfFilePath)
            
        if self.mainWindow == None:
            return

        self.run_subprocess(pdfViewerCmd,background=True)

        if self.mainWindow != None: 
            if self.controller.editorList[currentIdx].textScreen.showMessages == True:
                self.controller.editorList[currentIdx].textScreen.toggle_message_btn()
            
    def view_html(self):
        '''
        uses webbrowser to open the report
        '''

        ## variables
        if self.mainWindow != None:
            self.mainWindow.ensure_tab_is_current()

        isTemplate = self.is_template()
        if isTemplate == True:
            return

        currentIdx = self.controller.currentFileIndex
        filePath = self.controller.filePathList[currentIdx]
        filePathBase = os.path.split(filePath)[0]
        fileName = self.controller.fileNameList[currentIdx]
        dirPath = self.controller.ensure_dir_present(filePath)
        
        ## error checking
        isActive = self.is_active_project(filePath)
        if not isActive:
            return

        ## clear the text
        if self.mainWindow != None:
            editor = self.mainWindow.controller.editorList[currentIdx] 
            editor.clear_messages()

        ## open the file in a browser 
        if re.search("\.rnw|\.nw",fileName,flags=re.IGNORECASE):
            htmlFilePath = os.path.join(dirPath,re.sub("\.rnw|\.nw",".html",fileName,flags=re.IGNORECASE))
        else:
            sl = SphinxLogger(os.path.join(dirPath,'sphinx.log'))
            htmlFilePath = os.path.join(dirPath,"_build",'index.html')

        if not os.path.exists(htmlFilePath):
            errMsg = "'%s' does not exist.<p>Try HTML compilation again"%(os.path.split(htmlFilePath)[-1])
            self.display_error(errMsg)
            return

        webbrowser.open_new("file://"+os.path.realpath(htmlFilePath))

        if self.mainWindow != None: 
            if self.controller.editorList[currentIdx].textScreen.showMessages == True:
                self.controller.editorList[currentIdx].textScreen.toggle_message_btn()
