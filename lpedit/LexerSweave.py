
import sys,re
from PyQt4 import QtGui, QtCore, Qsci
from KeywordsLatex import latexKeywords
from KeywordsR import rKeywords

class LexerSweave(Qsci.QsciLexerCustom):
    """
    A custom lexer for sweave programming

    """

    def __init__(self, parent,latexColor="#FF4400",rColor="#0066FF",sweaveColor="#9900CC"):
        Qsci.QsciLexerCustom.__init__(self, parent)
        self._styles = { 
            0: 'Default',
            1: 'latexkw',
            2: 'sweavekw',
            3: 'rkw',
            4: 'comment',
            5: 'math',
            6: 'digits'
            }
        self.latexColor = latexColor
        self.rColor = rColor
        self.sweaveColor = sweaveColor
        self.isMath = False

        ## get compiled latex pattern
        self.patLatex = self.get_compiled_latex_pattern()
        self.patR = self.get_compiled_r_pattern()

        for key,value in self._styles.iteritems():
            setattr(self, value, key)

    def get_compiled_latex_pattern(self):
        #pat = ""
        #for kw in latexKeywords.iterkeys():
        #    pat += "|" + kw
        #pat = r"%s"%pat[1:]
        pat = r"\\.+\[|\\.+\{"
        cpat = re.compile(pat)
        return cpat

    def get_compiled_r_pattern(self):
        pat = ""
        for kw in rKeywords.iterkeys():
            pat += "|" + kw

        pat = r"%s"%pat[1:]
        cpat = re.compile(pat)
        return cpat

    def language(self):
        return 'Config Files'

    def description(self, style):
        return self._styles.get(style, '')

    def defaultColor(self, style):
        if style == self.Default:
            return QtGui.QColor('#000000')
        elif style == self.latexkw:
            return QtGui.QColor(self.latexColor)
        elif style == self.sweavekw:
            return QtGui.QColor(self.sweaveColor)
        elif style == self.comment:
            return QtGui.QColor('#333333')
        elif style == self.rkw:
            return QtGui.QColor(self.rColor)
        elif style == self.digits:
            return QtGui.QColor('#000000')
        elif style == self.math:
            return QtGui.QColor('#000000')

        return Qsci.QsciLexerCustom.defaultColor(self, style)

    def defaultFont(self, style):
        font = Qsci.QsciLexerCustom.defaultFont(self, style)

        if style in [self.latexkw,self.sweavekw,self.rkw]:
            font.setBold(True)
            #font.setUnderline(True)

        return font

    def defaultPaper(self,style):
        """
        change the color of the background.
        """

        if style == self.comment:
            return QtGui.QColor('#CCCCCC')
        #elif style == self.sweavekw:
        #    return QtGui.QColor('#FFFF99')
        #elif style == self.digits:
        #    return QtGui.QColor('#FFCC66')
        if style == self.math:
            return QtGui.QColor('#66FF66')

        return Qsci.QsciLexerCustom.defaultPaper(self, style)

    def defaultEolFill(self, style):
        """
        colorize background of a line.
        """
        if style == self.sweavekw:
          return True
        return Qsci.QsciLexerCustom.defaultEolFill(self, style)

    def toggle_math(self):
        """
        toggle the math mode
        """

        if self.isMath == True:
            self.isMath = False
        else:
            self.isMath = True
        
    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

        SCI = editor.SendScintilla
        set_style = self.setStyling

        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            source = bytearray(end - start)
            SCI(Qsci.QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
        if not source:
            return

        self.startStyling(start, 0x1f)

        index = SCI(Qsci.QsciScintilla.SCI_LINEFROMPOSITION, start)
        self.isSweave = False

        ## control the styling of each linja
        lineCount = -1
        self.sweaveLines = []
        for linja in source.splitlines(True):
            length = len(linja)
            i = 0
            newState = None
            allChars = []
            texChars = []
            lineCount +=1 
            if self.isSweave == True:
                self.sweaveLines.append(lineCount)

            ## skip blank lines
            #if not re.search("\w|\#|\%|\.",linja):
            #    pass
            ## style the comments
            if re.search("^\%",linja):
                newState = self.comment
            ## style line indicating code start
            elif re.search('^<<',linja):
                self.isSweave = True
                newState = self.sweavekw
            ## style line indicating code end
            elif linja.startswith('@'):
                self.isSweave = False
                newState = self.sweavekw
            ## style the LaTex keywords
            elif self.patLatex.search(r"%s"%linja):
                print 'colored by elif', linja
                allChars = []
                for m in self.patLatex.finditer(r"%s"%linja):
                    allChars.extend(range(m.start(0),m.end(0)))
                texChars = list(set(allChars))
                #print "is there a return", re.search("\R",lin

                while i < length:
                    #pos = SCI(Qsci.QsciScintilla.SCI_GETLINEENDPOSITION, index) - length + 1
                    pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index) - length + 1
                    self.startStyling(i+pos,0x1f)
                    if chr(linja[i]) == '$':
                        self.toggle_math()

                    if re.search("\[|\]|\{|\}",chr(line[i])):
                        newState = self.Default
                    elif i in texChars:
                        newState = self.latexkw
                    elif self.isMath == True:
                        newState = self.math
                    else:
                        newState = self.Default
                 
                    set_style(i,newState)
                    i+=1
                newState = None

            ## style the r keywords
            elif self.patR.search(r"%s"%linja) and lineCount in self.sweaveLines:
                allChars = []
                for m in self.patR.finditer(r"%s"%linja):
                    allChars.extend(range(m.start(0),m.end(0)))
                allChars = list(set(allChars))
         
                while i < length:          ##CHANGE
                    pos = SCI(Qsci.QsciScintilla.SCI_GETLINEENDPOSITION, index) - length + 1
                    self.startStyling(i + pos, 0x1f)
                    if i in allChars:
                        newState = self.rkw
                    else:
                        newState = self.Default
                
                    set_style(pos,newState)
                    i+=1
                newState = None
            else:
                print 'colored by else', linja
                while i < length:
                    pos = SCI(Qsci.QsciScintilla.SCI_GETLINEENDPOSITION, index) - length + 1
                    self.startStyling(i+pos,0x1f)
                    if chr(linja[i]) == '$':
                        self.toggle_math()
                
                    if re.search("\[|\]|\{|\}",chr(linja[i])):
                        newState = self.Default
                    elif i in texChars:
                        newState = self.latexkw
                    elif self.isMath == True:
                        newState = self.math
                    else:
                        newState = self.Default
                 
                    set_style(i,newState)
                    i+=1
                newState = None
                #while i < length:
                #    pos = SCI(Qsci.QsciScintilla.SCI_GETLINEENDPOSITION, index) - length + 1
                #    self.startStyling(i + pos, 0x1f)
                #    if chr(linja[i]) == '$':
                #        self.toggle_math()
                #        
                #    if self.isMath == True:
                #        if chr(linja[i]) == '$':
                #            newState = self.Default
                #        else:
                #            newState = self.math
                #    else:
                #        newState = self.Default
                # 
                #    set_style(1,newState)
                #    i+=1
                #newState = None
               
            if newState:
                set_style(length, newState)

            index += 1

        ## reset
        self.newState = self.Default
        self.isMath = False
