#!/usr/bin/python

'''
lpEdit
Logger

'''

__author__ = "A Richards"

import os,csv,re,ast
from version import __version__

defaultLog = {
    'python_path': None,
    'latex_path':None,
    'pdfviewer_path':None,
    'r_path':None,
    'sphinx_path':None,
    'latex2html_path':None,
    'font_size':10,
    'font_family':'sans',
    'default_lang': 'r',
    'embed_color': '#CC0000',
    'markup_color': '#0000CC',
    'math_color': '#FF9900',
    'comment_color': '#888888',
    'default_report': 'PDF'
}

class Logger():
    '''
    Logger class to handle the logging user specified defaults
    '''

    def __init__(self):
        '''
        constructor
        '''

        self.logFileDir = os.path.join(os.path.expanduser('~'),".lpEdit")
        if os.path.exists(self.logFileDir) == True and os.path.isdir(self.logFileDir) == False:
            os.remove(self.logFileDir)
        
        if os.path.isdir(self.logFileDir) == False:
            os.mkdir(self.logFileDir)

        self.logFilePath = os.path.join(self.logFileDir,"lpEdit-%s.log"%(re.sub("\.","-",__version__)))

        if os.path.exists(self.logFilePath) == False:
            writer = csv.writer(open(self.logFilePath,'w'))
            
            for key,item in defaultLog.iteritems():
                if item == None:
                    item = 'None'
                elif type(item) != type('i am a string'):
                    item = str(item)

                writer.writerow([key,item])

        self.log = self.read_project_log(self.logFilePath)
        
    ## effectivly the only action necessary to save a project in its current state
    def write(self):
        writer = csv.writer(open(self.logFilePath,'w'))

        for key,item in self.log.iteritems():
            if item == None:
                item = 'None'
            elif type(item) != type('i am a string'):
                item = str(item)

            writer.writerow([key,item])
            
    ## reads the log file assciated with the current project and returns a dict
    def read_project_log(self,logPathName):
        
        if os.path.isfile(logPathName) == False:
            print "ERROR: invalid model logfile specified",logPathName
            return None
        else:
            logFileDict = {}
            reader = csv.reader(open(logPathName,'r'))
            for linja in reader:

                if re.search("\[|\{|None",str(linja[1])):
                    try:
                        linja[1] = ast.literal_eval(str(linja[1]))
                    except:
                        print 'ERROR: Logger -- string literal conversion failed', linja[1]

                logFileDict[linja[0]] = linja[1]

            return logFileDict
