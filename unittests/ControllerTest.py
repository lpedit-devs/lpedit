#!/usr/bin/env python

import sys,os,unittest
import matplotlib as mpl
if mpl.get_backend() != 'agg':
    mpl.use('agg')
from lpEdit import Controller

## test class for the main window function
class ControllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = Controller(debug=False)
        self.examplesDir = os.path.realpath(os.path.join(self.controller.baseDir,'examples'))

    def testSanitize(self):
        self.assertFalse(self.controller.sanitize_check("rm *"))
        self.assertTrue(self.controller.sanitize_check("python blah blah"))

    def testPythonPath(self):
        pythonPath = self.controller.get_python_path()
        self.assertTrue(os.path.exists(pythonPath))
                
    def testAddingFiles(self):
        self.controller.reset_all()
        ## load file
        fileName1 = "FishersExactTest.Rnw"
        filePath1 = os.path.join(self.examplesDir,fileName1)
        self.assertTrue(os.path.exists(filePath1))
        isValid = self.controller.load_file(filePath1)
        self.assertTrue(isValid)
        self.assertEqual(self.controller.filePathList[0],filePath1)
        self.assertEqual(self.controller.fileNameList[0],fileName1)

        ## try loading same file
        self.assertFalse(self.controller.load_file(filePath1,verbose=False))

        ## load another file
        fileName2 = "SimpleHeatmap.Rnw"
        filePath2 = os.path.join(self.examplesDir,fileName2)
        self.assertTrue(os.path.exists(filePath1))
        self.controller.load_file(filePath2)
        self.assertEqual(self.controller.filePathList[1],filePath2)
        self.assertEqual(self.controller.fileNameList[1],fileName2)
    
    def testRemovingFiles(self):
        self.controller.reset_all()
        fileName = "FishersExactTest.Rnw"
        filePath = os.path.join(self.examplesDir,fileName)
        self.assertTrue(os.path.exists(filePath))
        isValid = self.controller.load_file(filePath)
        self.assertTrue(isValid)
        self.assertEqual(self.controller.filePathList[0],filePath)
        self.assertEqual(self.controller.fileNameList[0],fileName)
        
        self.controller.remove_file(fileName)
        self.assertEqual(self.controller.get_number_active_files(),0)
     
    def testLogging(self):
        originalValue = self.controller.log.log['python_path']
        self.controller.log.log['python_path'] = "/usr/bin/python"
        self.controller.save()
        self.assertEqual("/usr/bin/python",self.controller.log.log['python_path'])
        self.controller.log.log['python_path'] = originalValue
        self.controller.save()
        self.assertEqual(originalValue,self.controller.log.log['python_path'])

### Run the tests
if __name__ == '__main__':
    unittest.main()
