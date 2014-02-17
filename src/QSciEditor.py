#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os,re
from PyQt4 import QtGui, QtCore,Qsci
from PyQt4.Qsci import QsciLexerPython
from TextScreen import TextScreen
from KeywordsLatex import latexKeywords
from KeywordsR import rKeywords
from KeywordsPython import pythonKeywords
from KeywordsRest import restKeywords
from CustomLexer import CustomLexer

class QSciEditor(QtGui.QWidget):
    def __init__(self, parent=None,mainWindow=None):
        QtGui.QWidget.__init__(self,parent)

        ## declare variables
        self.mainWindow = mainWindow
        self.initialized = False

        ## setup layout
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.setAlignment(QtCore.Qt.AlignCenter)
        self.hbl = QtGui.QHBoxLayout()
        self.hbl.setAlignment(QtCore.Qt.AlignCenter)
        self.hb2 = QtGui.QHBoxLayout()
        self.hb2.setAlignment(QtCore.Qt.AlignCenter)
       
        ## defaults
        if self.mainWindow != None:
            self.fontSize = self.mainWindow.controller.log.log['font_size']
        else:
            self.fontSize = 10

        self.fontType = 'Courier'

        ## add qsci editing component
        self.init_editor()

        self.hbl.addWidget(self.editor)

        ## add the std output screen
        self.textScreen = TextScreen()
        self.hb2.addWidget(self.textScreen)

        ## sets as default a minimized std output screen
        self.textScreen.toggle_message_btn()

        ## finalize layout
        self.vbl.addLayout(self.hbl)
        self.vbl.addLayout(self.hb2)
        self.setLayout(self.vbl)

        ## testing without mainWindow
        if self.mainWindow == None:
            self.showMaximized()
            exampleFilePath = os.path.join(os.getcwd(),'examples','FishersExactTest.Rnw') 
            self.set_lexer(fileName=exampleFilePath)
            self.load_text(exampleFilePath)

    def init_editor(self):
        self.editor = Qsci.QsciScintilla()
        
        self.set_font()
        self.initialized = True
        
        self.fm = QtGui.QFontMetrics(self.font)
        self.editor.setFont(self.font)
        self.editor.setMarginsFont(self.font)
        self.editor.setUtf8(True)
        
        ## margins
        self.editor.setMarginWidth(0, self.fm.width( "00000" ) + 5)
        self.editor.setMarginLineNumbers(0, True)

        ## setup margins 
        self.editor.setMarginsFont(self.font)
        self.editor.setMarginWidth(0, self.fm.width("00000") + 6)
        self.editor.setMarginLineNumbers(0, True)

        ## margin coloring
        self.editor.setMarginsBackgroundColor(QtGui.QColor("#333333"))
        self.editor.setMarginsForegroundColor(QtGui.QColor("#CCCCCC"))
        self.editor.setFoldMarginColors(QtGui.QColor("#99CC66"),QtGui.QColor("#333300"))
        #self.editor.setWrapVisualFlags(Qsci.QsciScintilla.WrapFlagByBorder)
        
        ## Indentation
        self.editor.setIndentationWidth(4)
        self.editor.setTabWidth(4) 
        self.editor.setIndentationGuides(True)
        self.editor.setIndentationGuidesForegroundColor(QtGui.QColor("#111111"))
        
        # 80-columns edge
        self.editor.setEdgeColumn(80)
        #self.editor.setEdgeMode(Qsci.QsciScintilla.EdgeLine)
        
        ######################################

        # Current line visible with special background color
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QtGui.QColor("#FFE4E4"))

        ## Folding visual : we will use boxes
        self.editor.setFolding(Qsci.QsciScintilla.BoxedTreeFoldStyle)

        ## Braces matching
        self.editor.setBraceMatching(Qsci.QsciScintilla.SloppyBraceMatch)

        ## wrap mode
        self.editor.setWrapMode(True)
        self.editor.setWrapMode(Qsci.QsciScintilla.WrapWord)
        self.editor.setWrapVisualFlags(True)
        #self.editor.setWrapMode(QsciScintilla.WrapWord if enable
        #                        else QsciScintilla.WrapNone)
       
        ## connect to QScintilla signals
        self.connect(self.editor,QtCore.SIGNAL('textChanged()'),
                     self.set_editing_mode)
        
    def set_editing_mode(self):
        if self.mainWindow != None:
            self.mainWindow.set_editing_mode()

    def zoom_in(self):
        self.editor.zoomIn(5)
    def zoom_out(self):
        self.editor.zoomOut(5)
        
    def clear_messages(self):
        self.textScreen.clear_text()

    def set_font(self):
        if self.mainWindow != None:
            self.fontSize = self.mainWindow.controller.log.log['font_size']
        else:
            self.fontSize = 10

        ## set the default font of the editor
        font = QtGui.QFont()
        font.setFamily(self.fontType)
        font.setFixedPitch(True)
        font.setPointSize(int(self.fontSize))

        ## and take the same font for line numbers
        self.editor.setFont(font)
        self.editor.setMarginsFont(font)
        self.font = font

    def set_lexer(self,fileName=None,lexer=None):
        """
        sets the custom lexer for the editor
        """

        if self.mainWindow == None:
            currentIdx = 0
            fileLang = 'r'
        else:
            currentIdx = self.mainWindow.tabWidget.currentIndex()
            fileLang = self.mainWindow.controller.fileLangList[currentIdx]

        if re.search("\.rnw|\.nw",fileName,flags=re.IGNORECASE):
            lexer = CustomLexer(self.editor,'latex',fileLang,mainWindow=self.mainWindow)
            self.language1 = 'latex'
        elif re.search("\.rst",fileName,flags=re.IGNORECASE):
            lexer = CustomLexer(self.editor,'rest',fileLang,mainWindow=self.mainWindow)
            self.language1 = 'rest'
        else:
            print "WARNING: QSciEditor could not identify language 1"

        lexer.setDefaultFont(self.font)
        self.lexer = lexer
        self.editor.setLexer(lexer)

        ## used to style the comments
        self.editor.SendScintilla(Qsci.QsciScintilla.SCI_STYLESETFONT,1,self.fontType)
        self.editor.setFoldMarginColors(QtGui.QColor("#99CC66"),QtGui.QColor("#333300"))
        
        # add auto complete
        if self.language1 == 'latex':
            self.enable_auto_complete(lexer)

    def enable_auto_complete(self,lexer):
        ## Create an API for us to populate with our autocomplete terms
        api = Qsci.QsciAPIs(lexer)
        
        ## Add autocompletion strings
        #if isSweave == True:
        for key,value in latexKeywords:
            kw = r"%s"%re.sub("^\\\\+","",key)
            value= r"%s"%re.sub("^\\\\+","",value)
            api.add(QtCore.QString(value))

        ## Compile the api for use in the lexer
        api.prepare()
        self.editor.setAutoCompletionThreshold(2)
        self.editor.setAutoCompletionSource(Qsci.QsciScintilla.AcsAPIs)
        
    def load_text(self,text):
        '''
        loads text either from a file or as a given string
        '''

        ## Show this file in the editor
        if os.path.exists(text):
            self.editor.setText(open(text).read())
        else:
            self.editor.setText(text)

    def get_text(self):
        '''
        gets current text
        '''
        currentText = self.editor.text()
        
        return str(currentText)
        
### Run the tests 
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    qse = QSciEditor()
    qse.show()
    sys.exit(app.exec_())
