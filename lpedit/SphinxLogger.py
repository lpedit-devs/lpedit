#!/usr/bin/python

'''
lpEdit
sphinx log

'''

__author__ = "A Richards"

import os,csv,re,ast
from version import __version__
from PyQt4 import QtGui

defaultLog = {
    'project_name': 'Untitled',
    'version': '1.0',
    'release': '1.0',
    'authors':  'author names',
    'html_title': 'Untitled',
    'html_theme': 'default',
    'html_show_copyright': True,
    'latex_preamble': '\usepackage{bm,amsmath}',
    'latex_pointsize': '11pt',
    'latex_papersize': 'a4paper',
    'extensions':  ['sphinx.ext.pngmath'],
}

class SphinxLogger():
    '''
    Logger class to handle the logging user specified defaults
    '''

    def __init__(self,logFilePath,mainWindow=None):
        '''
        constructor
        '''
        
        self.logFilePath = logFilePath
        self.mainWindow = mainWindow

        ## load or create logfile
        if os.path.exists(self.logFilePath) == False:
            writeFile = open(self.logFilePath,'w')
            writer = csv.writer(writeFile)

            for key,item in defaultLog.iteritems():
                if item == None:
                    item = 'None'
                elif type(item) != type('i am a string'):
                    item = str(item)

                writer.writerow([key,item])
            writeFile.close()

        self.log = self.read_project_log(self.logFilePath)

    ## effectivly the only action necessary to save a project in its current state
    def write(self):
        '''
        writes the dict log to its associated file 
        '''

        writer = csv.writer(open(self.logFilePath,'w'))

        for key,item in self.log.iteritems():
            if item == None:
                item = 'None'
            elif type(item) != type('i am a string'):
                item = str(item)

            writer.writerow([key,item])

    ## reads the log file assciated with the current project and returns a dict
    def read_project_log(self,logPathName):
        '''
        reads the dict log from a log file path name
        '''

        if os.path.isfile(logPathName) == False:
            print "ERROR: invalid model logfile specified",logPathName
            return None
        else:
            logFileDict = {}
            reader = csv.reader(open(logPathName,'r'))
            for linja in reader:
                if linja[0] == 'latex_preamble':
                    pass
                elif re.search("\[|\{|None",str(linja[1])):
                    try:
                        linja[1] = ast.literal_eval(str(linja[1]))
                    except:
                        print 'ERROR: Logger -- string literal conversion failed', linja[1]

                logFileDict[linja[0]] = linja[1]

            return logFileDict


### Run the tests
if __name__ == '__main__':

    sphinxLog = SphinxLogger('sphinx.log')
    print sphinxLog.log.keys()
