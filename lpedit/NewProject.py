#!/usr/bin/python

'''
lpEdit 
NewProject.py

'''

__author__ = "A Richards"

import sys,time,csv,os,re
from PyQt4 import QtGui, QtCore

class NewProject(QtGui.QWidget):
    def __init__(self,templatesDir,mainWindow=None,parent=None,fontSize=11):

        self.w = QtGui.QWidget.__init__(self,parent)
        
        if mainWindow == None:
            self.resize(850, 700)
            self.move(350, 100)

        if os.path.exists(templatesDir) == False:
            print "ERROR: bad templates dir passed to NewProject.py"

        templatesList = []
        for tname in os.listdir(templatesDir):
            if re.search('~|\.pyc',tname):
                continue
            if re.search("\.DS",tname):
                continue
            if tname == ("__init__.py"):
                continue
            templatesList.append(tname)

        ## arg variables
        self.templatesDir = templatesDir
        self.templatesList = templatesList
        self.setWindowTitle('New project')
        self.mainWindow = mainWindow
        self.fontSize = fontSize
        self.order = 'orig'
        self.btnColor = QtGui.QColor(255, 204, 153)
        
        ## provide some order for the templates
        knownTemplates = ["BasicSweave.rnw","PlotsInSweave.rnw","BasicPython.nw","PlotsInPython.nw"]
        for tpl in knownTemplates:
            if self.templatesList.__contains__(tpl):
                self.templatesList.remove(tpl)

        self.templatesList = knownTemplates + self.templatesList
        
        ## double check that there are no directories in the templates dir
        for filePath in self.templatesList:
            if os.path.isdir(os.path.join(self.templatesDir,filePath)):
                self.templatesList.remove(filePath)

        ## prepare layout
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignTop)
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.setAlignment(QtCore.Qt.AlignTop)

        ## create the layout
        self.init_table()

        #finalize layout
        vbox.addLayout(self.hbox)
        self.setLayout(vbox)
        
    def init_table(self):
        ## setup layouts
        ssLayout = QtGui.QVBoxLayout()
        ssLayout.setAlignment(QtCore.Qt.AlignCenter)
        ssLayout1 = QtGui.QHBoxLayout()
        ssLayout1.setAlignment(QtCore.Qt.AlignCenter)
        ssLayout2 = QtGui.QHBoxLayout()
        ssLayout2.setAlignment(QtCore.Qt.AlignCenter)
        
        ## set up the label
        self.chksSummaryLabel = QtGui.QLabel('Create a new file')

        ## determine the order
        templateList = []
        for tName in self.templatesList:
            templateList.append(tName)
        if self.order == 'alph':
            templateList.sort()

        templateList = templateList

        ## initialize table widget
        self.table = QtGui.QTableWidget(len(templateList),3,parent=self)
        self.table.setHorizontalHeaderLabels(QtCore.QStringList()
                                             << self.tr('Template name')
                                             << self.tr('Document type')
                                             << self.tr('Description'))
        # table behavior
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.backcolor1 = QtGui.QColor("#99FFCC")
        self.backcolor2 = QtGui.QColor("#FFFFFF")
        self.cTypeBoxes = {}
        for row,tname in enumerate(templateList):
            nameItem = QtGui.QTableWidgetItem(tname)
            
            ## get description
            if self.mainWindow != None:
                templatePath = os.path.join(self.templatesDir,tname)
                fh = open(templatePath,'r')
                firstLine = fh.next()
                fh.close()
                if re.search("^[\%|#|\.\.]",firstLine):
                    desc = re.sub("^[\%|#|\.\.]","",firstLine)
                    desc = re.sub("^\W+","",desc)
                else:
                    desc = 'template does not provide description'
            else:
                desc = 'foo'

            descItem = QtGui.QTableWidgetItem(desc)
            if re.search('\.rnw|\.Rnw',tname,flags=re.IGNORECASE):
                progItem = QtGui.QTableWidgetItem('Sweave')
            elif re.search('\.nw',tname,flags=re.IGNORECASE):
                progItem = QtGui.QTableWidgetItem('noweb')
            elif re.search('\.rst',tname,flags=re.IGNORECASE):
                progItem = QtGui.QTableWidgetItem('reST')
            else:
                progItem = QtGui.QTableWidgetItem('unknown')

            self.table.setItem(row,0,nameItem)
            self.table.setItem(row,1,progItem)
            self.table.setItem(row,2,descItem)
            
        self.table.selectRow(0)
        
        ## column sizes
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.showMaximized()
        self.table.horizontalHeader().setStretchLastSection(True)

        ## finalize layouts
        ssLayout1.addWidget(self.chksSummaryLabel)
        ssLayout2.addWidget(self.table)
        ssLayout.addLayout(ssLayout1)
        ssLayout.addLayout(ssLayout2)
        self.hbox.addLayout(ssLayout)

    def get_selected(self):
        '''
        return the selected row

        '''
        currentIndex = self.table.currentRow()
        row=[]
        for j in range(3):
            row.append(str(self.table.item(currentIndex,j).text()))

        return row

    def generic_callback(self):
        print "generic callback"

### Run the tests
if __name__ == '__main__':    
    app = QtGui.QApplication(sys.argv)

    templatesDir = os.path.join(os.path.dirname(__file__),'templates')
    dpc = NewProject(templatesDir)
    dpc.show()
    sys.exit(app.exec_())
    
