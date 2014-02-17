#!/usr/bin/env python


import sys,os,unittest
import matplotlib as mpl
if mpl.get_backend() != 'agg':
    mpl.use('agg')
from lpEdit import Controller,NoGuiAnalysis

## test class for the main window function
class FishersExactTest(unittest.TestCase):
    def setUp(self):
        controller = Controller(debug=False)        
        self.examplesDir = os.path.realpath(os.path.join(controller.baseDir,'examples'))
        self.baseFileName = "FishersExactTest"
        fileName = self.baseFileName + ".Rnw"
        filePath = os.path.join(self.examplesDir,fileName)
        self.nga = NoGuiAnalysis(controller)
        self.nga.load_file(filePath)

    def testScript(self):
        '''
        generic test script for files in the examples folder
        '''

        ## test compile sweave
        verbose = False
        filePath = self.nga.controller.filePathList[0]
        self.nga.clean_file(filePath)
        self.nga.compile_code(verbose=verbose)
        texFilePath = os.path.join(self.examplesDir,self.baseFileName,self.baseFileName+".tex")
        self.assertTrue(os.path.exists(texFilePath))

        ## test compile LaTeX
        self.nga.compile_latex(verbose=verbose)
        pdfFilePath = os.path.join(self.examplesDir,self.baseFileName+".pdf")
        self.assertTrue(os.path.exists(pdfFilePath))

### Run the tests
if __name__ == '__main__':
    unittest.main()
