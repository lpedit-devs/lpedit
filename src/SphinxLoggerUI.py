import sys,os,re,ast
from PyQt4 import QtGui, QtCore
from SphinxLogger import SphinxLogger
from FileUploader import FileUploader
from BasicWidgets import Tooltip

class SphinxLoggerUI(QtGui.QWidget):
    """
    GUI wrapper class for SphinxLogger.py

    The purpose of this class is to interface and edit basic elements of a conf.py file.
    
    For more information on the Sphinx conf.py file:
    http://sphinx-doc.org/config.html

    """

    def __init__(self, sphinxLog, parent=None, mainWindow=None):
        QtGui.QWidget.__init__(self,parent)

        ## variables
        self.sphinxLog = sphinxLog
        self.mainWindow = mainWindow

        if self.mainWindow == None:
            screen = QtGui.QDesktopWidget().screenGeometry()
            self.screenWidth = screen.width()
            self.screenHeight = screen.height()
        else:
            self.screenWidth = self.mainWindow.screenWidth
            self.screenHeight = self.mainWindow.screenHeight

        ## setup layout
        self.mainBox = QtGui.QVBoxLayout()
        self.mainBox.setAlignment(QtCore.Qt.AlignTop)
        self.grid = QtGui.QGridLayout()
        
        ## init the UI
        self.init_ui()
        self.refresh_values()

    def init_ui(self):
        """
        Initialize the user interface
        """

        ## set the labels
        self.infoBox = QtGui.QHBoxLayout()
        self.infoBox.setAlignment(QtCore.Qt.AlignCenter)

        self.infoBoxLabel = QtGui.QLabel('Sphinx Project Configuration')
        self.infoBox.addWidget(self.infoBoxLabel)

        self.col1Label = QtGui.QLabel('General')
        self.grid.addWidget(self.col1Label,0,0)

        self.col2Label = QtGui.QLabel('LaTeX and HTML')
        self.grid.addWidget(self.col2Label,0,2)

        ## project name
        self.nameEdit = QtGui.QLineEdit()
        self.nameEdit.setText(str(self.sphinxLog.log['project_name']))
        self.nameLabel = QtGui.QLabel('Project name:')
        self.grid.addWidget(self.nameLabel,1,0)
        self.grid.addWidget(self.nameEdit,1,1)
        self.nameTip = Tooltip(msg="The name of the project",parent=self.nameEdit)

        ## version
        self.versionEdit = QtGui.QLineEdit()
        self.versionEdit.setText(str(self.sphinxLog.log['version']))
        self.versionLabel = QtGui.QLabel('Version:')
        self.grid.addWidget(self.versionLabel,2,0)
        self.grid.addWidget(self.versionEdit,2,1)
        self.versionTip = Tooltip(msg="Project version: for example,'1.0'",parent=self.versionEdit)

        ## release
        self.releaseEdit = QtGui.QLineEdit()
        self.releaseLabel = QtGui.QLabel('Release:')
        self.grid.addWidget(self.releaseLabel,3,0)
        self.grid.addWidget(self.releaseEdit,3,1)
        self.releaseTip = Tooltip(msg="Project release: for example,'1.0'",parent=self.releaseEdit)

        ## authors
        self.authorsEdit = QtGui.QLineEdit()
        self.authorsLabel = QtGui.QLabel('Authors:')
        self.grid.addWidget(self.authorsLabel,4,0)
        self.grid.addWidget(self.authorsEdit,4,1)
        msg = "Project authors (comma delim): for example, 'Thomas Bayes, Pierre-Simon Laplace'"
        self.authorsTip = Tooltip(msg=msg,parent=self.authorsEdit)

        ## extensions
        self.extensionsEdit = QtGui.QTextEdit()
        self.extensionsLabel = QtGui.QLabel('Extensions:')
        self.grid.addWidget(self.extensionsLabel,6,0)
        self.grid.addWidget(self.extensionsEdit,6,1)
        msg = "Project extensions (Python list): for example, '['sphinx.ext.autodoc', 'sphinx.ext.pngmath']'"
        self.extensionsTip = Tooltip(msg=msg,parent=self.extensionsEdit)

        ## html title
        self.htmlTitleEdit = QtGui.QLineEdit()
        self.htmlTitleLabel = QtGui.QLabel("HTML title:")
        self.grid.addWidget(self.htmlTitleLabel,1,2)
        self.grid.addWidget(self.htmlTitleEdit,1,3)
        self.htmlTitleTip = Tooltip(msg='Title of the HTML document',parent=self.htmlTitleEdit)

        ## html theme
        self.htmlThemeEdit = QtGui.QLineEdit()
        self.htmlThemeLabel = QtGui.QLabel("HTML theme:")
        self.grid.addWidget(self.htmlThemeLabel,2,2)
        self.grid.addWidget(self.htmlThemeEdit,2,3)
        msg = "HTML Theme (choose one): 'default', 'scrolls','sphinxdoc','agogo','nature','traditional','pyramid','haiku'"
        self.htmlThemeTip = Tooltip(msg=msg,parent=self.htmlThemeEdit)

        self.htmlShowCopyrightEdit = QtGui.QLineEdit()
        self.htmlShowCopyrightLabel = QtGui.QLabel("HTML show copyright:")
        self.grid.addWidget(self.htmlShowCopyrightLabel,3,2)
        self.grid.addWidget(self.htmlShowCopyrightEdit,3,3)
        msg = "Show the copyright in the footer (choose one): 'True', 'False'"
        self.htmlShowCopyrightTip = Tooltip(msg=msg,parent=self.htmlShowCopyrightEdit)

        ## latex point size
        self.texPointSizeEdit = QtGui.QLineEdit()
        self.texPointSizeLabel = QtGui.QLabel('LaTeX point size:')
        self.grid.addWidget(self.texPointSizeLabel,4,2)
        self.grid.addWidget(self.texPointSizeEdit,4,3)
        self.texPointSizeTip = Tooltip(msg="LaTeX point size: for example, '10pt' or '12pt'",parent=self.texPointSizeEdit)

        ## latex paper size
        self.texPaperSizeEdit = QtGui.QLineEdit()
        self.texPaperSizeLabel = QtGui.QLabel("LaTeX paper:")
        self.grid.addWidget(self.texPaperSizeLabel,5,2)
        self.grid.addWidget(self.texPaperSizeEdit,5,3)
        self.texPaperSizeTip = Tooltip(msg="LaTeX paper size: for example, 'letterpaper' or 'a4paper'",parent=self.texPaperSizeEdit)

        ## latex preamble
        self.texPreambleEdit = QtGui.QTextEdit()
        self.texPreambleLabel = QtGui.QLabel("LaTeX preamble:")
        self.grid.addWidget(self.texPreambleLabel,6,2)
        self.grid.addWidget(self.texPreambleEdit,6,3)
        self.texPreambleTip = Tooltip(msg="Lines to be added to the preamble: for example, '\usepackage{bm}'",parent=self.texPreambleEdit)

        #self.fontSizeWidget = QtGui.QSpinBox()
        #self.fontSizeWidget.setValue(int(self.log.log['font_size']))
        #self.fontSizeWidget.setMinimum(1)
        #self.fontSizeWidget.setMaximum(24)
        
        ## finalize layout
        self.mainBox.addLayout(self.infoBox)
        self.mainBox.addWidget(QtGui.QLabel(' '))
        self.mainBox.addWidget(QtGui.QLabel(' '))
        self.mainBox.addLayout(self.grid)
        self.setLayout(self.mainBox)


    def refresh_values(self):
        '''
        refreshes the values from the log file in the appropriate fields
        '''

        self.nameEdit.setText(str(self.sphinxLog.log['project_name']))
        self.versionEdit.setText(str(self.sphinxLog.log['version']))
        self.releaseEdit.setText(str(self.sphinxLog.log['release']))
        self.authorsEdit.setText(str(self.sphinxLog.log['authors']))
        self.extensionsEdit.setText(str(self.sphinxLog.log['extensions']))
        self.htmlTitleEdit.setText(str(self.sphinxLog.log['html_title']))
        self.htmlThemeEdit.setText(str(self.sphinxLog.log['html_theme']))
        self.htmlShowCopyrightEdit.setText(str(self.sphinxLog.log['html_show_copyright']))
        self.texPointSizeEdit.setText(str(self.sphinxLog.log['latex_pointsize']))
        self.texPaperSizeEdit.setText(str(self.sphinxLog.log['latex_papersize']))
        self.texPreambleEdit.setText(str(self.sphinxLog.log['latex_preamble']))

    def save_callback(self):
        """
        saves all the fields in the ui to the corresponding SphinxLogger file
        """

        self.sphinxLog.log['project_name'] = str(self.nameEdit.text())
        self.sphinxLog.log['release'] = str(self.releaseEdit.text())
        self.sphinxLog.log['version'] = str(self.versionEdit.text())
        self.sphinxLog.log['authors'] = str(self.authorsEdit.text())
        self.sphinxLog.log['extensions'] = ast.literal_eval(str(self.extensionsEdit.toPlainText()))
        self.sphinxLog.log['preamble'] = str(self.authorsEdit.text())
        self.sphinxLog.log['html_title'] = str(self.htmlTitleEdit.text())
        self.sphinxLog.log['html_theme'] = str(self.htmlThemeEdit.text())
        self.sphinxLog.log['html_show_copyright'] = ast.literal_eval(str(self.htmlShowCopyrightEdit.text()))
        self.sphinxLog.log['latex_papersize'] = str(self.texPaperSizeEdit.text())
        self.sphinxLog.log['latex_pointsize'] = str(self.texPointSizeEdit.text())
        self.sphinxLog.log['latex_preamble'] = str(self.texPreambleEdit.toPlainText())

        self.sphinxLog.write()
        self.refresh_values()

        if self.mainWindow != None:
            self.mainWindow.display_info("Sphinx config file has been updated.")

## show the ui
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    sphinxLog = SphinxLogger('sphinx.log')
    bp = SphinxLoggerUI(sphinxLog)
    bp.showMaximized()
    bp.raise_()
    bp.show()
    bp.save_callback()

    os.remove('sphinx.log')
    sys.exit(app.exec_())
    
