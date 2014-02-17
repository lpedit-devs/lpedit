#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os,re
import sys
from PyQt4 import QtCore, QtGui
import unicodedata

def main():
    app = QtGui.QApplication(sys.argv)
    w = TextScreen()
    w.show()
    sys.exit(app.exec_())

class TextScreen(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)


        ## variables
        self.codec = QtCore.QTextCodec.codecForName("UTF-8")

        ## create screen part
        self.allLines = []
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setReadOnly(True)

        # change text to white
        self.textEdit.setTextColor(QtGui.QColor("#FFFFFF"))

        # change the background to black
        palette = QtGui.QPalette()
        bgc = QtGui.QColor(0, 0, 0)
        palette.setColor(QtGui.QPalette.Base, bgc)
        textc = QtGui.QColor(255, 255, 255)
        palette.setColor(QtGui.QPalette.Text, textc)
        self.setPalette(palette)

        ## create toggle button
        self.toggleBtn = QtGui.QPushButton("Toggle Messages", self)
        self.toggleBtn.setMaximumWidth(350)
        self.toggleBtn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.connect(self.toggleBtn,QtCore.SIGNAL('clicked()'), self.toggle_message_btn)
        self.showMessages = True
        self.textEdit.setVisible(self.showMessages)

        # finalize layout
        self.vb1 = QtGui.QVBoxLayout(self)
        self.hb1 = QtGui.QHBoxLayout()
        self.hb1.setAlignment(QtCore.Qt.AlignCenter)
        self.hb2 = QtGui.QHBoxLayout()
        self.hb2.setAlignment(QtCore.Qt.AlignCenter)

        self.hb1.addWidget(self.textEdit)
        self.hb2.addWidget(self.toggleBtn)
        self.vb1.addLayout(self.hb1)
        self.vb1.addLayout(self.hb2)
        self.setLayout(self.vb1)

        ## add start text
        self.add_text("Waiting to proceed...")

    def add_text(self,txt):
        self.allLines.append(txt)
        toWrite = ''
        for line in self.allLines:
            line = "\n%s"%line
            toWrite += line

        self.textEdit.setText(toWrite)

    def clear_text(self):
        self.allLines = []
        self.textEdit.setText('')

    def toggle_message_btn(self):
        if self.showMessages == True:
            self.showMessages = False
        else:
            self.showMessages = True
        
        self.textEdit.setVisible(self.showMessages)

if __name__ == "__main__":
    main()
