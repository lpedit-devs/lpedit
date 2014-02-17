#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os,sys,re
from PyQt4 import QtCore, QtGui

def main():
    app = QtGui.QApplication(sys.argv)
    w = TextScreen()
    w.show()
    sys.exit(app.exec_())

class DocumentViewer(QtGui.QWidget):
    def __init__(self, filePath, mainWindow=None):
        QtGui.QWidget.__init__(self)

        ## error checking
        if os.path.exists(filePath) == False:
            errMsg = "Cannot open document viewer: invalid file path"
            if self.mainWindow != None:
                self.mainWindow.display_warning(errMsg)
            else:
                print errMsg
            return

        ## variables
        self.filePath = filePath
        self.mainWindow = mainWindow
        self.setWindowTitle(self.filePath)


        ## create screen part
        self.allLines = []
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setReadOnly(True)

        # change text to white
        #self.textEdit.setTextColor(QtGui.QColor("#FFFFFF"))

        # change the background to black
        #palette = QtGui.QPalette()
        #bgc = QtGui.QColor(0, 0, 0)
        #palette.setColor(QtGui.QPalette.Base, bgc)
        #textc = QtGui.QColor(255, 255, 255)
        #palette.setColor(QtGui.QPalette.Text, textc)
        #self.setPalette(palette)

        ## create buttons
        self.closeBtn = QtGui.QPushButton("Close", self)
        self.closeBtn.setMaximumWidth(350)
        self.closeBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connect(self.closeBtn,QtCore.SIGNAL('clicked()'), self.close_callback)
        
        self.refreshBtn = QtGui.QPushButton("Refresh", self)
        self.refreshBtn.setMaximumWidth(350)
        self.refreshBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connect(self.refreshBtn,QtCore.SIGNAL('clicked()'), self.refresh)

        # finalize layout
        self.vb1 = QtGui.QVBoxLayout(self)
        self.hb1 = QtGui.QHBoxLayout()
        self.hb1.setAlignment(QtCore.Qt.AlignCenter)
        self.hb2 = QtGui.QHBoxLayout()
        self.hb2.setAlignment(QtCore.Qt.AlignCenter)

        self.hb1.addWidget(self.textEdit)
        self.hb2.addWidget(self.refreshBtn)
        self.hb2.addWidget(self.closeBtn)
        self.vb1.addLayout(self.hb1)
        self.vb1.addLayout(self.hb2)
        self.setLayout(self.vb1)

        ## add text
        self.refresh()

    def refresh(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.textEdit.setText('')
        self.textEdit.setText(open(self.filePath).read())
        QtGui.QApplication.restoreOverrideCursor()                

    def close_callback(self):
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    filePath = __file__
    dv = DocumentViewer(filePath)
    dv.show()
    dv.showMaximized()
    sys.exit(app.exec_())
