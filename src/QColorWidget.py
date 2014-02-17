#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A dialog to change the font colors
"""

import sys
from PyQt4 import QtGui,QtCore

class QColorWidget(QtGui.QWidget):

    def __init__(self, parent=None, mainWindow=None, defaultColor="#000000"):
        QtGui.QWidget.__init__(self,parent)
        
        self.initUI()
        self.currentColor = None
        self.set_color(defaultColor)
        self.setAutoFillBackground(True)

    def set_color(self,colorName):
        palette = self.palette()
        role = self.backgroundRole()
        palette.setColor(role, QtGui.QColor(colorName))
        self.setPalette(palette)
        
        self.currentColor = colorName
        QtCore.QCoreApplication.processEvents()

    def initUI(self):

        ## layout
        self.mainBox = QtGui.QVBoxLayout()
        self.mainBox.setAlignment(QtCore.Qt.AlignCenter)
        hbox = QtGui.QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignLeft)

        self.btn = QtGui.QPushButton('Choose', self)
        self.btn.clicked.connect(self.show_dialog)
        hbox.addWidget(self.btn)

        ## finalize layout
        self.mainBox.addLayout(hbox)
        self.setLayout(self.mainBox)

    def show_dialog(self):      
        selectedColor = QtGui.QColorDialog.getColor()
        if not selectedColor.isValid():
            return

        self.set_color(selectedColor.name())
        


def main():    
    app = QtGui.QApplication(sys.argv)
    ex = QColorWidget()
    ex.show()
    ex.raise_()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
