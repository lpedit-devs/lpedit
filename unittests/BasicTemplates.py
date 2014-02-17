#!/usr/bin/env python


import sys,os,time,unittest,shutil,re
from lpedit import Controller,NoGuiAnalysis
from lpedit import SphinxLogger

## test class for the main window function
class BasicTemplates(unittest.TestCase):
    def setUp(self):
        self.controller = Controller(debug=False)        
        self.templatesDir = os.path.realpath(os.path.join(self.controller.baseDir,'templates'))
        self.examplesDir = os.path.realpath(os.path.join(self.controller.baseDir,'examples'))
        self.verbose = False

    def load_template(self,baseFileName,fileExtension,fileLang):
        self.baseFileName = baseFileName
        fileName = self.baseFileName + fileExtension
        _filePath = os.path.join(self.templatesDir,fileName)
        filePath = os.path.join(self.examplesDir,fileName)
        shutil.copy(_filePath,filePath)

        if  re.search("\.rst",fileName,flags=re.IGNORECASE):
            self.projectDir = os.path.join(self.examplesDir,"_sphinx")
        else:
            self.projectDir = os.path.join(self.examplesDir,"_latex")

        self.nga = NoGuiAnalysis(self.controller)
        self.nga.clean_file(filePath)
        self.nga.load_file(filePath,fileLang=fileLang)
    
    
    def testSweave(self):
        '''
        generic test script for files in the examples folder
        '''

        self.load_template("BasicSweave",".rnw",'r')

        ## test compile sweave
        filePath = self.nga.controller.filePathList[0]
        self.nga.build(verbose=self.verbose)
        texFilePath = os.path.join(self.projectDir,self.baseFileName+".tex")
        self.assertTrue(os.path.exists(texFilePath))

        ## test compile LaTeX
        self.nga.compile_pdf(verbose=self.verbose)
        pdfFilePath = os.path.join(self.examplesDir,self.baseFileName+".pdf")
        self.assertTrue(os.path.exists(pdfFilePath))

    def testNwR(self):
        '''
        generic test script for files in the examples folder
        '''

        self.load_template("BasicSweave",".rnw",'r')

        ## test compile sweave
        filePath = self.nga.controller.filePathList[0]
        self.nga.build(verbose=self.verbose)
        texFilePath = os.path.join(self.projectDir,self.baseFileName+".tex")
        self.assertTrue(os.path.exists(texFilePath))

        ## test compile LaTeX
        self.nga.compile_pdf(verbose=self.verbose)
        pdfFilePath = os.path.join(self.examplesDir,self.baseFileName+".pdf")
        self.assertTrue(os.path.exists(pdfFilePath))


    def testNwPython(self):
        '''
        generic test script for files in the examples folder
        '''

        self.load_template("BasicPython",".nw",'python')

        ## test compile sweave
        filePath = self.nga.controller.filePathList[0]
        self.nga.build(verbose=self.verbose)
        texFilePath = os.path.join(self.projectDir,self.baseFileName+".tex")
        self.assertTrue(os.path.exists(texFilePath))

        ## test compile LaTeX to pdf
        self.nga.compile_pdf(verbose=self.verbose)
        pdfFilePath = os.path.join(self.examplesDir,self.baseFileName+".pdf")
        self.assertTrue(os.path.exists(pdfFilePath))

        latex2htmlPath = self.controller.get_latex2html_path()
        if latex2htmlPath == None:
            print "WARNING: latex2html path does not exist skipping test"
            return

        ## test compile LaTeX to html
        self.nga.compile_html(verbose=self.verbose)
        time.sleep(1)
        htmlFilePath = os.path.join(self.examplesDir,"_latex",self.baseFileName,"index.html")
        self.assertTrue(os.path.exists(htmlFilePath))

    def testRstPython(self):
        '''
        generic test script for files in the examples folder
        '''

        self.load_template("BasicPython",".rst",'python')
        
        ## test building with sphinx
        self.nga.build(verbose=self.verbose)
        sl = SphinxLogger(os.path.join(self.projectDir,'sphinx.log'))
        
        ## test compile LaTeX
        self.nga.compile_pdf(verbose=self.verbose)
        texFileName = sl.log['project_name'] + ".tex"
        texFilePath = os.path.join(self.projectDir,"_build",texFileName)
        self.assertTrue(os.path.exists(texFilePath))
        pdfFileName = sl.log['project_name'] + ".pdf"
        pdfFilePath = os.path.join(self.examplesDir,pdfFileName)
        self.assertTrue(os.path.exists(pdfFilePath))

        ## test compile html
        self.nga.compile_html(verbose=self.verbose)
        indexFilePath = os.path.join(self.projectDir,"_build","index.html")
        self.assertTrue(os.path.exists(indexFilePath))

    def testRstR(self):
        '''
        generic test script for files in the examples folder
        '''

        self.load_template("BasicR",".rst",'r')
        
        ## test building with sphinx
        self.nga.build(verbose=self.verbose)
        sl = SphinxLogger(os.path.join(self.projectDir,'sphinx.log'))
        
        ## test compile LaTeX
        self.nga.compile_pdf(verbose=self.verbose)
        texFileName = sl.log['project_name'] + ".tex"
        texFilePath = os.path.join(self.projectDir,"_build",texFileName)
        self.assertTrue(os.path.exists(texFilePath))
        pdfFileName = sl.log['project_name'] + ".pdf"
        pdfFilePath = os.path.join(self.examplesDir,pdfFileName)
        self.assertTrue(os.path.exists(pdfFilePath))

        ## test compile html
        self.nga.compile_html(verbose=self.verbose)
        indexFilePath = os.path.join(self.projectDir,"_build","index.html")
        self.assertTrue(os.path.exists(indexFilePath))

### Run the tests
if __name__ == '__main__':
    unittest.main()
