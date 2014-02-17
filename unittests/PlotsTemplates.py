#!/usr/bin/env python


import sys,os,unittest,shutil,re
import matplotlib as mpl
if mpl.get_backend() != 'agg':
    mpl.use('agg')
from lpedit import Controller,NoGuiAnalysis

## test class for the main window function
class PlotsTemplates(unittest.TestCase):
    def setUp(self):
        self.controller = Controller(debug=False)        
        self.templatesDir = os.path.realpath(os.path.join(self.controller.baseDir,'templates'))
        self.examplesDir = os.path.realpath(os.path.join(self.controller.baseDir,'examples'))

    def testPlotsInSweave(self):
        '''
        generic test script for files in the examples folder
        '''

        self.baseFileName = "PlotsInSweave"
        fileName = self.baseFileName + ".rnw"
        _filePath = os.path.join(self.templatesDir,fileName)
        filePath = os.path.join(self.examplesDir,fileName)

        ## load project
        self.nga = NoGuiAnalysis(self.controller)
        self.nga.clean_file(filePath)
        shutil.copy(_filePath,filePath)
        self.nga.load_file(filePath)

        ## test compile sweave
        verbose = False
        filePath = self.nga.controller.filePathList[0]
        self.nga.build(verbose=verbose)
        texFilePath = os.path.join(self.examplesDir,self.baseFileName,self.baseFileName+".tex")
        self.assertTrue(os.path.exists(texFilePath))

        ## test compile LaTeX
        self.nga.compile_latex(verbose=verbose)
        pdfFilePath = os.path.join(self.examplesDir,self.baseFileName+".pdf")
        self.assertTrue(os.path.exists(pdfFilePath))

    def testPlotsInPythonNoweb(self):
        '''
        generic test script for files in the examples folder
        '''

        self.baseFileName = "PlotsInPython"
        fileName = self.baseFileName + ".nw"
        _filePath = os.path.join(self.templatesDir,fileName)
        filePath = os.path.join(self.examplesDir,fileName)
        
        ## load project
        self.nga = NoGuiAnalysis(self.controller)
        self.nga.clean_file(filePath)
        shutil.copy(_filePath,filePath)
        self.nga.load_file(filePath,fileLang='python')

        ## test compile sweave
        verbose = False
        filePath = self.nga.controller.filePathList[0]
        self.nga.build(verbose=verbose)
        texFilePath = os.path.join(self.examplesDir,self.baseFileName,self.baseFileName+".tex")
        self.assertTrue(os.path.exists(texFilePath))

        ## test compile LaTeX
        self.nga.compile_latex(verbose=verbose)
        pdfFilePath = os.path.join(self.examplesDir,self.baseFileName+".pdf")
        self.assertTrue(os.path.exists(pdfFilePath))
    
### Run the tests
if __name__ == '__main__':
    unittest.main()
