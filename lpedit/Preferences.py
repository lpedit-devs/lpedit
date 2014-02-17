import sys,os,time,re
from PyQt4 import QtGui, QtCore
from Logging import Logger
from FileUploader import FileUploader
from BasicWidgets import Tooltip
from QColorWidget import QColorWidget
from Logging import defaultLog

class Preferences(QtGui.QWidget):
    """
    Main preferences user interface.

    The main purpose is to be able to set default paths for 
    R, Python, pdflatex, sphinx-build, and a pdfviewer

    """

    def __init__(self, parent=None, mainWindow=None):
        QtGui.QWidget.__init__(self,parent)

        ## variables
        self.mainWindow = mainWindow

        if self.mainWindow == None:
            screen = QtGui.QDesktopWidget().screenGeometry()
            self.screenWidth = screen.width()
            self.screenHeight = screen.height()
            self.log = Logger()
        else:
            self.screenWidth = self.mainWindow.screenWidth
            self.screenHeight = self.mainWindow.screenHeight
            self.log = self.mainWindow.controller.log

        ## handle defaults
        for preference in ['pdfviewer_path','r_path','latex_path','sphinx_path','python_path','latex2html_path']:
            if self.log.log[preference] == None and self.mainWindow != None:
                self.log.log[preference] = self.get_default(preference)
                self.mainWindow.controller.save()

        ## setup layout
        self.mainBox = QtGui.QVBoxLayout()
        self.mainBox.setAlignment(QtCore.Qt.AlignTop)
        self.grid = QtGui.QGridLayout()
        self.grid.setColumnMinimumWidth (0, int(round(0.35 * self.screenWidth)))
        self.grid.setColumnMinimumWidth (1, int(round(0.15 * self.screenWidth)))
        self.grid.setColumnMinimumWidth (2, int(round(0.2 * self.screenWidth)))
        self.grid.setColumnMinimumWidth (3, int(round(0.2 * self.screenWidth)))

        self.init_ui()
        self.refresh_values()

    def init_ui(self):
        """
        Initialize the user interface
        """
        
        ## labels
        self.infoBox = QtGui.QHBoxLayout()
        self.infoBox.setAlignment(QtCore.Qt.AlignCenter)

        self.infoBoxLabel = QtGui.QLabel('lpEdit Preferences')
        self.infoBox.addWidget(self.infoBoxLabel)

        self.col1Label = QtGui.QLabel('Application Preferences')
        self.grid.addWidget(self.col1Label,0,0)

        self.col2Label = QtGui.QLabel('Editor Preferences')
        self.grid.addWidget(self.col2Label,0,2)

        ## application preference widgets
        self.pdfviewWidget = FileUploader(mainLabel="PDF Viewer")
        self.grid.addWidget(self.pdfviewWidget,1,0)
        self.pdfviewWidget.connect_help(self.pdfview_help)

        self.latexPathWidget = FileUploader(mainLabel="LaTeX Path")
        self.grid.addWidget(self.latexPathWidget,2,0)
        self.latexPathWidget.connect_help(self.latex_help)

        self.rPathWidget = FileUploader(mainLabel="R Path")
        self.grid.addWidget(self.rPathWidget,3,0)
        self.rPathWidget.connect_help(self.r_help)

        self.pythonPathWidget = FileUploader(mainLabel="Python Path")
        self.grid.addWidget(self.pythonPathWidget,4,0)
        self.pythonPathWidget.connect_help(self.python_help)

        self.sphinxPathWidget = FileUploader(mainLabel="Sphinx Path")
        self.grid.addWidget(self.sphinxPathWidget,5,0)
        self.sphinxPathWidget.connect_help(self.sphinx_help)

        self.latex2htmlPathWidget = FileUploader(mainLabel="LaTeX2HTML Path")
        self.grid.addWidget(self.latex2htmlPathWidget,6,0)
        self.latex2htmlPathWidget.connect_help(self.latex2html_help)

        ## put an empty widget in the spacer column
        self.spacerMiddle = QtGui.QLabel("")
        self.grid.addWidget(self.spacerMiddle,0,1)

        ## editor preference widgets
        self.fontSizeLabel = QtGui.QLabel("Default font size:")
        self.fontSizeWidget = QtGui.QSpinBox()
        self.fontSizeWidget.setMinimum(1)
        self.fontSizeWidget.setMaximum(24)
        self.grid.addWidget(self.fontSizeLabel,1,2)
        self.grid.addWidget(self.fontSizeWidget,1,3)
        self.fontSizeTip = Tooltip(msg="Changes the default editor font size",
                                       parent=self.fontSizeWidget)

        self.lang1ColorLabel = QtGui.QLabel("Markup language color:")
        self.lang1ColorWidget = QColorWidget(parent=self)
        self.grid.addWidget(self.lang1ColorLabel,2,2)
        self.grid.addWidget(self.lang1ColorWidget,2,3)
        self.lang1ColorTip = Tooltip(msg="Changes the markup language highlight color",
                                       parent=self.lang1ColorWidget)

        self.lang2ColorLabel = QtGui.QLabel("Embedded language color:")
        self.lang2ColorWidget = QColorWidget(parent=self)
        self.grid.addWidget(self.lang2ColorLabel,3,2)
        self.grid.addWidget(self.lang2ColorWidget,3,3)
        self.lang2ColorTip = Tooltip(msg="Changes the embedded language highlight color",
                                       parent=self.lang2ColorWidget)

        self.mathColorLabel = QtGui.QLabel("Math color:")
        self.mathColorWidget = QColorWidget(parent=self)
        self.grid.addWidget(self.mathColorLabel,4,2)
        self.grid.addWidget(self.mathColorWidget,4,3)
        self.mathColorTip = Tooltip(msg="Changes the math highlight color",
                                    parent=self.mathColorWidget)


        self.commentColorLabel = QtGui.QLabel("Comment color:")
        self.commentColorWidget = QColorWidget(parent=self)
        self.grid.addWidget(self.commentColorLabel,5,2)
        self.grid.addWidget(self.commentColorWidget,5,3)
        self.commentColorTip = Tooltip(msg="Changes the math highlight color",
                                       parent=self.commentColorWidget)

        ## finalize layout
        self.mainBox.addLayout(self.infoBox)
        self.mainBox.addWidget(QtGui.QLabel(' '))
        self.mainBox.addWidget(QtGui.QLabel(' '))
        self.mainBox.addLayout(self.grid)
        self.setLayout(self.mainBox)

    def refresh_values(self):
        """
        refreshes all the fields on preferences page
        """

        self.pythonPathWidget.update_path(self.log.log['python_path'])
        self.rPathWidget.update_path(self.log.log['r_path'])
        self.latexPathWidget.update_path(self.log.log['latex_path'])
        self.latex2htmlPathWidget.update_path(self.log.log['latex2html_path'])
        self.pdfviewWidget.update_path(self.log.log['pdfviewer_path'])
        self.sphinxPathWidget.update_path(self.log.log['sphinx_path'])
        self.fontSizeWidget.setValue(int(self.log.log['font_size']))
        self.commentColorWidget.set_color(self.log.log['comment_color'])
        self.mathColorWidget.set_color(self.log.log['math_color'])
        self.lang1ColorWidget.set_color(self.log.log['markup_color'])
        self.lang2ColorWidget.set_color(self.log.log['embed_color'])

    def get_default(self,preference):
        """
        returns the default for a given preference
        """

        if self.mainWindow == None and re.search('path',preference):
            return '/some/path'
        elif preference == 'pdfviewer_path':
            return self.mainWindow.controller.get_pdfviewer_path()                
        elif preference == 'r_path':
            return self.mainWindow.controller.get_r_path()
        elif preference == 'python_path':
            return self.mainWindow.controller.get_python_path()
        elif preference == 'latex_path':
            return self.mainWindow.controller.get_latex_path()
        elif preference == 'latex2html_path':
            return self.mainWindow.controller.get_latex2html_path()
        elif preference == 'sphinx_path':
            return self.mainWindow.controller.get_sphinx_path()
        elif defaultLog.has_key(preference):
            return defaultLog[preference]
        else:
            print "ERROR: tried to get invalid preference default in Preferences.py"
            print "...", preference

    def is_valid_path(self,appName,appPath):
        """
        Checks to see if an application path is valid
        """
        
        if appPath == None:
            return False

        msg = "The %s path does not exist\n\n%s\n\nChange not saved"%(appName, appPath)
        if appPath in ['open','/some/path']:
            return True
        if os.path.exists(appPath) == False:
            self.mainWindow.display_warning(msg)
            return False

        return True

    def restore_defaults_callback(self):
        """
        restores all preferences to original values
        """

        ## application paths
        for preference in ['pdfviewer_path','r_path','latex_path','sphinx_path','python_path','latex2html_path']:
            self.log.log[preference] = self.get_default(preference)

        ## editor preferences
        for preference in ['font_size','embed_color','markup_color','math_color','comment_color']:
                self.log.log[preference] = self.get_default(preference)

        if self.mainWindow != None:
            self.mainWindow.controller.save()
            self.mainWindow.display_info("Default preferences have been restored.")
            self.mainWindow.transitions.reload_tabs()
            self.mainWindow.transitions.move_to_preferences()
            self.refresh_values()

    def save_callback(self):
        """
        callback to save all preferences
        """

        print 'saving...'

        ## application paths
        pythonPath = self.pythonPathWidget.get_path()
        check = self.is_valid_path("python path", pythonPath)
        if check == True:
            self.log.log['python_path'] = pythonPath

        rPath = self.rPathWidget.get_path()
        check = self.is_valid_path("r_path", rPath)
        if check == True:
            self.log.log['r_path'] = rPath

        latexPath =  self.latexPathWidget.get_path()
        check = self.is_valid_path("latex_path",latexPath)  
        if check == True:
            self.log.log['latex_path'] = latexPath

        pdfviewerPath = self.pdfviewWidget.get_path()
        check = self.is_valid_path("pdfviewer_path", pdfviewerPath)  
        if check == True:
            self.log.log['pdfviewer_path'] = pdfviewerPath

        sphinxPath = self.sphinxPathWidget.get_path()
        check = self.is_valid_path("sphinx_path", sphinxPath)
        if check == True:
            self.log.log['sphinx_path'] = sphinxPath

        latex2htmlPath = self.latex2htmlPathWidget.get_path()
        check = self.is_valid_path("latex2html_path", latex2htmlPath)
        if check == True:
            self.log.log['latex2html_path'] = sphinxPath
        
        ## editor colors
        self.log.log['comment_color'] = str(self.commentColorWidget.currentColor)
        self.log.log['math_color'] = str(self.mathColorWidget.currentColor)
        self.log.log['markup_color'] = str(self.lang1ColorWidget.currentColor)
        self.log.log['embed_color'] = str(self.lang2ColorWidget.currentColor)

        ## font size
        fontSize = str(self.fontSizeWidget.text())
        isValidFont = True
        try:
            fontSize = int(fontSize)
        except:
            isValidFont = False
            self.mainWindow.display_warning("Invalid font specified.")

        if isValidFont == False:
            return
         
        self.log.log['font_size'] = fontSize

        if self.mainWindow != None:
            self.mainWindow.controller.save()
            self.mainWindow.display_info("Changes have been saved.")
            self.mainWindow.transitions.reload_tabs()
            self.mainWindow.transitions.move_to_preferences()

    def sphinx_help(self):
        """
        Shows a message box with help for sphinx
        """

        QtGui.QMessageBox.about(self, "Sphinx",
                                """To learn more about Sphinx visit the <a href='%s'>homepage </a>.      
                                In lpEdit Sphinx is used for literate programming via Python.

                                <p> Sphinx can however be used for most languages, but code 
                                cannot be evaluated at compile time.

                                <p> Most users will not have to change this path, but if you do use the 
                                path to <i>sphinx-build</i>.  For example <i>/usr/bin/sphinx-build</i>.

                                """ %("http://sphinx-doc.org"))
    def r_help(self):
        QtGui.QMessageBox.about(self, "R",
                                """R (<a href='%s'>official site</a>) needs to be installed in order 
                                     to use the Sweave portion of lpEdit.  lpEdit does not install R for you.  

                                   <p> For your convenience:

                                   <ul>
                                     <li><a href='http://cran.r-project.org/bin/macosx'>Installing on OS X</a></li>
                                     <li><a href='http://cran.r-project.org/bin/windows/base'>Installing on Windows</a></li>
                                     <li><a href='http://cran.r-project.org/bin/linux/ubuntu/README'>Installing on Ubuntu</a></li>
                                   </ul>
  
                                   lpEdit will work with any version of R that is 2.4.1 or newer.
                                """ %("http://www.r-project.org"))

    def latex_help(self):
        QtGui.QMessageBox.about(self, "LaTeX",
                                """LaTeX (<a href='%s'>official site</a>) needs to be installed in order 
                                     to use lpEdit (both for Sweave and reST).  lpEdit does not install LaTeX
                                     for you.  

                                   <p> For your convenience:

                                   <ul>
                                     <li><a href='http://www.tug.org/mactex'>Installing on OS X</a></li>
                                     <li><a href='http://mactex-wiki.tug.org/wiki/index.php/TeX_Distributions'>Alternative installs for OS X</a></li>
                                     <li><a href='http://www.miktex.org'>Installing on Windows (MikTeX)</a></li>
                                     <li><a href='http://www.tug.org/protext'>Installing on Windows (proTeXt)</a></li>
                                     <li><a href='https://help.ubuntu.com/community/LaTeX'>Installing on Ubuntu</a></li>
                                   </ul>
                                """ %("http://www.latex-project.org"))

    def pdfview_help(self):
        QtGui.QMessageBox.about(self, "PDF viewer",
                                """You may change the default PDF viewer that lpEdit uses by changing the path here.<p> 
                                   <i>Adobe reader</i> may be used, but there are others like: <i>okular</i>, 
                                   <i>evince</i>, <i>GhostView</i>, and <i>Xpdf</i>.  lpEdit does not install a PDF 
                                   viewer for you. 

                                   <p> On windows systems the file path for adobe must end with something like 
                                   <i>AcroRd32.exe</i>.

                                   <p> On OS X systems the <i>open</i> command will call your default PDF viewer.
                                """ )
    def python_help(self):
        QtGui.QMessageBox.about(self, "Python",
                                """To learn more about Python visit the <a href=%s>homepage </a>.      
                                lpEdit is written in Python.  

                                <p> Changing this variable may make lpEdit unstable. Most users do not need to change this path, 
                                however, if you are working from source then this path must be valid.
                                """ %("http://python.org"))

    def latex2html_help(self):
        QtGui.QMessageBox.about(self, "latex2html",
                                """<a href=%s>latex2html</a> and <a href=%s>tth</a> are programs used to convert LaTeX into HTML.
                               
                                <p> These programs often need to be manually installed and they have limitations.  If the intended document form  is 
                                HTML it may be worth considering using reST.  
                                """ %("http://www.latex2html.org","http://hutchinson.belmont.ma.us/tth"))

    def font_dialog_callback(self):        
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            print 'setting font to ', font
            #self.lbl.setFont(font)

    def font_change_callback(self):
        if self.mainWindow == None:
            print 'font change callback does nothing without main window present'
            return

        fontSize = str(self.mainWindow.preferences.fontSizeWidget.text())
        isValidFont = True
        try:
            fontSize = int(fontSize)
        except:
            isValidFont = False
            self.mainWindow.display_warning("Invalid font selected")

        if isValidFont == False:
            return

        self.mainWindow.controller.log.log['font_size'] = fontSize
        self.mainWindow.controller.save()
        self.mainWindow.transitions.reload_tabs()
        self.mainWindow.display_info("Fonts have been updated.")


### Run the tests 
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    bp = Preferences(None)
    bp.show()
    bp.showMaximized()
    bp.raise_()
    sys.exit(app.exec_())
    
