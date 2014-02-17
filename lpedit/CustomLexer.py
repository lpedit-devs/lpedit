#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,re
from PyQt4 import QtCore, QtGui, Qsci
from KeywordsLatex import latexKeywords
from KeywordsR import rKeywords
from KeywordsPython import pythonKeywords
from KeywordsRest import restKeywords
from TextExamples import text1

class MainWindow(QtGui.QMainWindow):
    """
    simple main window class used for testing CustomLexer.py
    """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle('Custom Lexer Example')
        self.setGeometry(QtCore.QRect(50,200,400,400))
        self.editor = Qsci.QsciScintilla(self)
        self.editor.setUtf8(True)
        self.editor.setMarginWidth(2, 15)
        self.editor.setFolding(True)
        self.setCentralWidget(self.editor)
        self.lexer = CustomLexer(self.editor,'latex','python')
        #self.editor.setEdgeColumn(80)
        #self.editor.setEdgeMode(Qsci.QsciScintilla.EdgeLine)              
        self.editor.setLexer(self.lexer)
        self.editor.setText(text1)

class CustomLexer(Qsci.QsciLexerCustom):
    def __init__(self, parent,language1,language2, mainWindow=None):
        Qsci.QsciLexerCustom.__init__(self, parent)

        ## variables
        self.parent = parent
        self.language1 = language1
        self.language2 = language2
        self.isMath = False
        self.isComment = False
        self.mainWindow = mainWindow

        self._styles = {
            0: 'Default',
            1: 'Comment',
            2: 'Lang1',
            3: 'Lang2',
            4: 'CodeBorder',
            5: 'Math',
            }
        for key,value in self._styles.iteritems():
            setattr(self, value, key)

     
        ## set the languages
        self.set_languages()

        ## set colors
        self.defaultColor = '#000000'
        self.codeBorderColor = '#005533'
        self.mathBackground = "#FFFF00"

        if self.mainWindow != None:
            log = self.mainWindow.controller.log
            self.commentColor = log.log['comment_color']
            self.lang1Color = log.log['markup_color']
            self.lang2Color = log.log['embed_color']
            self.mathColor = log.log['math_color']
        else:
            self.commentColor = '#333333'
            self.lang1Color     = '#0000CC'
            self.lang2Color = '#CC0000'
            self.mathColor = '#FF9900'

    def set_languages(self):
        '''
        looks at language1 and language2 and sets the highlight vocab
        '''

        ## set the languages
        self.language1,self.language2 = self.language1.lower(),self.language2.lower()
        if self.language1 not in ['latex','rest']:
            print "ERROR: CustomLexer invalid language 1--", self.language1
        if self.language2 not in ['r','python']:
            print "ERROR: CustomLexer invalid language 2--", self.language2
         
        ## set language
        if self.language1 == 'latex':
            self.language1kws = latexKeywords
        elif self.language1 == 'rest':
            self.language1kws = restKeywords
        else:
            print "ERROR: CustomLexer language1 must be 'rest' or 'latex'"

        if self.language2 == 'r':
            self.language2kws = rKeywords
        elif self.language2 == 'python':
            self.language2kws = pythonKeywords
        else:
            print "ERROR: CustomLexer language2 must be 'r' or 'python'"
 
        ## take the keywords from a language and compile them to a re pattern
        pat = ""
        for kw in self.language1kws:
            pat += "|" + kw[0]
                            
        self.pattern1 = re.compile(pat[1:])
        
        pat = ""
        for kw in self.language2kws:
            pat += "|" + r"%s"%kw[0]

        self.pattern2 = re.compile(pat[1:])

    def description(self, style):
        return self._styles.get(style, '')

    def defaultColor(self,style):
        if style == self.Default:
            return QtGui.QColor(self.defaultColor)
        elif style == self.Comment:
            return QtGui.QColor(self.commentColor)
        elif style == self.Lang1:
            return QtGui.QColor(self.lang1Color)
        elif style == self.Lang2:
            return QtGui.QColor(self.lang2Color)
        elif style == self.CodeBorder:
            return QtGui.QColor(self.codeBorderColor)
        elif style == self.Math:
            return QtGui.QColor(self.mathColor)
        return Qsci.QsciLexerCustom.defaultColor(self, style)

    def defaultFont(self, style):
        font = Qsci.QsciLexerCustom.defaultFont(self, style)

        if style in [self.Lang1,self.Lang2,self.CodeBorder,self.Math]:
            font.setBold(True)

        return font

    def get_code_lines(self):
        """
        return the indices that are embedded code
        """

        currentText = self.parent.text()
        splitText = currentText.split("\n")
        codeLines = []
        codeFlag = False
        count = -1
        for line in splitText:
            count += 1
            if codeFlag == True:
                codeLines.append(count)
            if re.search('^<<|\@',"%s"%line):
                codeFlag = True
            if re.search('^\@',"%s"%line):
                codeFlag = False
                
        return codeLines

    def get_math_lines(self):
        """
        return the indices that are embedded code
        """
    
        currentText = self.parent.text()
        splitText = currentText.split("\n")
        mathLines = []
        mathFlag = False
        count = -1
        for line in splitText:
            count += 1
            if mathFlag == True:
                mathLines.append(count)
            if re.search('\$',"%s"%line) and mathFlag == False:
                mathFlag = True
            if re.search('\$',"%s"%line) and mathFlag == True:
                mathFlag = False

        return mathLines

    def get_source(self,start,end):
        """
        returns the text from the editor
        """

        editor = self.editor()
        if editor is None:
            return

        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            if sys.hexversion >= 0x02060000:
                source = bytearray(end - start)
                editor.SendScintilla(
                    editor.SCI_GETTEXTRANGE, start, end, source)
            else:
                source = unicode(editor.text()).encode('utf-8')[start:end]
        if not source:
            return

        return source

    def defaultPaper(self,style):
        """
        change the color of the background. 
        """
        #if style == self.Math:
        #    return QtGui.QColor(self.mathBackground)
        #if style == self.Lang1 and self.isMath == True:
        #    return QtGui.QColor(self.mathBackground)

        return Qsci.QsciLexerCustom.defaultPaper(self, style)

    def toggle_math(self):
        """
        toggle the math mode
        """

        if self.isMath == True:
            self.isMath = False
        else:
            self.isMath = True

    def toggle_comment(self):
        """
        toggle the comment mode
        """

        if self.isComment == True:
            self.isComment = False
        else:
            self.isComment = True

    def styleText(self,start,end):
        """
        main function used to style the text
        """

        editor = self.editor()
        if editor is None:
            return

        source = self.get_source(start,end)

        # determines if we are editing or not
        index = editor.SendScintilla(editor.SCI_LINEFROMPOSITION, start)
        if index < 0:
            return

        if index > 0:
            # the previous state may be needed for multi-line styling
            pos = editor.SendScintilla(editor.SCI_GETLINEENDPOSITION,index)
            state = editor.SendScintilla(editor.SCI_GETSTYLEAT, pos)
            self.startStyling(start, 0x1f)
        else:
            state = self.Default
        
        SCI = editor.SendScintilla
        set_style = self.setStyling
        self.isCode = True

        # loop through each line of the document
        multilineComment = False
        for line in source.splitlines(True):
            if re.search("\r|\n",line):
                line = re.sub("\r|\n+","",line)

            length = len(line)
            pos = SCI(Qsci.QsciScintilla.SCI_GETLINEENDPOSITION, index) - length
            allChars = []
            i=0

            # check for blank line
            if re.search("^\s*$",r"%s"%line):
                isBlank = True
            else:
                isBlank = False

            ## check to see if line is code
            lineNum = int("%s"%index)
            codeLines = self.get_code_lines()
            if lineNum in codeLines:
                isCode = True
            else:
                isCode = False

            ## check for newLine character
            if re.search("\n","%s"%line):
                hasNewline = True
            else:
                hasNewline = False
                                
            if multilineComment == True and isBlank == True:
                multilineComment = False

            ## handle comments   
            if multilineComment == True:
                self.isMath = False
                self.startStyling(pos,0x1f)
                set_style(length, self.Comment)
                multilineComment = True
            elif self.language1 == 'latex' and line.startswith('%'):
                self.isMath = False
                self.startStyling(pos,0x1f)
                set_style(length, self.Comment)
            elif self.language1 == 'rest' and re.search('^\.\.',r"%s"%line) and not re.search('::',r"%s"%line) and not re.search("^\.\.\s+\[.+\]",r"%s"%line):
                self.isMath = False
                self.startStyling(pos,0x1f)
                set_style(length, self.Comment)
                multilineComment = True
            elif self.language2 in ['r','python'] and line.startswith('#'):
                self.isMath = False
                self.startStyling(pos,0x1f)
                set_style(length, self.Comment)
            elif re.search('^<<|^\@',"%s"%line):
                self.isMath = False
                self.startStyling(pos,0x1f)
                set_style(length, self.CodeBorder)
            
            ## handle language 2
            elif isCode == True and self.pattern2.search(r"%s"%line):
                ## force the math mode off
                self.isMath = False

                ## find language 2 keywords
                for m in self.pattern2.finditer(r"%s"%line):
                    lineStr = "%s"%line
                    if lineStr[m.end(0)-1] == "(":
                        allChars.extend(range(m.start(0),m.end(0)-1))
                    else:
                        allChars.extend(range(m.start(0),m.end(0)))

                allChars = list(set(allChars))

                i = 0
                while i < length:
                    if i in allChars:
                        self.startStyling(pos+i,0x1f)
                        set_style(1,self.Lang2)
                    else:
                        self.startStyling(pos+i,0x1f)
                        set_style(1, self.Default)
                    i+=1
               
            ## handle lines with language 1
            elif self.pattern1.search(r"%s"%line):
                ## search for inline comments
                commentChars = []
                if self.language1 == 'latex' and not re.search(r"\\%",r"%s"%line) and re.search(r"%",r"%s"%line):
                    m = re.search(r"%",r"%s"%line)
                    commentChars = range(m.start(0),len(r"%s"%line))

                ## look for equation environments to toggle math mode
                if re.search(r"\{equation\}|\{align\}|\{eqnarray\}",r"%s"%line):
                    self.toggle_math()
                if re.search(r"begin\{equation\}|begin\{align\}|begin\{eqnarray\}",r"%s"%line):
                    beginMath = True
                    self.isMath = True
                else:
                    beginMath = False
                if re.search(r"end\{equation\}|end\{align\}|end\{eqnarray\}",r"%s"%line):
                    self.isMath = False

                ## search for highlighted text
                for m in self.pattern1.finditer(r"%s"%line):
                    lineStr = "%s"%line
                    if lineStr[m.end(0)-1] == "{":
                        allChars.extend(range(m.start(0),m.end(0)))
                    else:
                        allChars.extend(range(m.start(0),m.end(0)+1))
                
                i = 0
            
                while i < length:
                    if i in commentChars:
                       
                       if hasNewline == True:
                            self.startStyling(pos+i,0x1f)
                       else:
                           self.startStyling(pos+i-1,0x1f)
                       set_style(1,self.Comment)
                    elif self.language1 == 'latex' and chr(line[i]) == '$':
                        self.toggle_math()
                        self.startStyling(pos+i,0x1f)
                        set_style(1,self.Math)
                    elif i in allChars:
                        if hasNewline == True:
                            self.startStyling(pos+i,0x1f)
                        else:
                            self.startStyling(pos+i-1,0x1f)
                        set_style(1,self.Lang1)                        
                    elif not beginMath and self.isMath == True or chr(line[i]) == "$":
                        self.startStyling(pos+i,0x1f)
                        set_style(1,self.Math)
                    else:
                        self.startStyling(pos+i,0x1f)
                        set_style(1,self.Default)
                
                    i+=1               
            
            else:
                ## comment characters
                commentChars = []   
                if self.language1 == 'latex' and not re.search(r"\\%",r"%s"%line) and re.search(r"%",r"%s"%line):
                    m = re.search(r"%",r"%s"%line)
                    commentChars = range(m.start(0),len(r"%s"%line))

                ## look for equation environments to toggle math mode
                if re.search(r"begin\{equation\}|begin\{align\}|begin\{eqnarray\}",r"%s"%line):
                    beginMath = True
                    self.isMath = True
                else:
                    beginMath = False
                if re.search(r"end\{equation\}|end\{align\}|end\{eqnarray\}",r"%s"%line):
                    self.isMath = False

                i = 0
                
                while i < length:
                    if i in commentChars:
                        if hasNewline == True:
                            self.startStyling(pos+i,0x1f)
                        else:
                            self.startStyling(pos+i-1,0x1f)
                        set_style(1,self.Comment)
                    elif chr(line[i]) == '$':
                        self.toggle_math()
                        self.startStyling(pos+i,0x1f)
                        set_style(1,self.Math)
                    elif not beginMath and self.isMath == True or chr(line[i]) == "$":
                        self.startStyling(pos+i,0x1f)
                        set_style(1,self.Math)
                    else:
                        self.startStyling(pos+i,0x1f)
                        set_style(1,self.Default)
                    i+=1
                
            index += 1
    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.connect(app, QtCore.SIGNAL('lastWindowClosed()'),
                QtCore.SLOT('quit()'))
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())
