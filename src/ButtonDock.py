import os,sys,re,shutil
from PyQt4 import QtGui, QtCore
from BasicWidgets import Tooltip

class ButtonDock(QtGui.QWidget):

    def __init__(self, parent=None, mainWindow=None,appColor='black', buttonSize=35):
        QtGui.QWidget.__init__(self, parent)

        ## input variables
        self.buttonSize = buttonSize
        self.mainWindow = mainWindow

        ## declared variables
        self.buff = 2.0
        self.btnColor = QtGui.QColor(255, 204, 153)
        self.mode = None

        ## init widgets 
        self.init_buttons()

        ## color
        palette = self.palette()
        role = self.backgroundRole()
        palette.setColor(role, QtGui.QColor(appColor))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def init_buttons(self):
        ## setup layout
        
        hbl = QtGui.QVBoxLayout()
        hboxLeft = QtGui.QHBoxLayout()
        hboxLeft.setAlignment(QtCore.Qt.AlignLeft)
        hboxRight = QtGui.QHBoxLayout()
        hboxRight.setAlignment(QtCore.Qt.AlignRight)

        vboxBottom = QtGui.QHBoxLayout()
        vboxBottom.addLayout(hboxLeft)
        vboxBottom.addLayout(hboxRight)
        vboxBottom.setAlignment(QtCore.Qt.AlignBottom)

        ## compile code btn
        self.compileCodeBtn = QtGui.QPushButton("Build Project")
        self.compileCodeBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.compileCodeBtn, QtCore.SIGNAL('clicked()'),self.compile_code_btn_callback)
        hboxLeft.addWidget(self.compileCodeBtn)
        
        ## build latex btn
        self.compileReportBtn = QtGui.QPushButton("Compile Report")
        self.compileReportBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.compileReportBtn, QtCore.SIGNAL('clicked()'),self.compile_report_btn_callback)
        hboxLeft.addWidget(self.compileReportBtn)
            
        ## view report btn
        self.viewReportBtn = QtGui.QPushButton("View Report")
        self.viewReportBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.viewReportBtn, QtCore.SIGNAL('clicked()'),self.view_report_btn_callback)
        hboxLeft.addWidget(self.viewReportBtn)

        ## return btn
        self.returnBtn = QtGui.QPushButton("Return")
        self.returnBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.returnBtn, QtCore.SIGNAL('clicked()'),self.return_btn_callback)
        hboxLeft.addWidget(self.returnBtn)

        ## save btn
        self.saveBtn = QtGui.QPushButton("Save Changes")
        self.saveBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.saveBtn, QtCore.SIGNAL('clicked()'),self.save_btn_callback)
        hboxLeft.addWidget(self.saveBtn)

        ## restore defaults btn
        self.restoreDefaultsBtn = QtGui.QPushButton("Restore Defaults")
        self.restoreDefaultsBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.restoreDefaultsBtn, QtCore.SIGNAL('clicked()'),self.restore_defaults_btn_callback)
        hboxLeft.addWidget(self.restoreDefaultsBtn)

        ## load btn
        self.loadBtn = QtGui.QPushButton("Load Selected")
        self.loadBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.loadBtn, QtCore.SIGNAL('clicked()'),self.load_btn_callback)
        hboxLeft.addWidget(self.loadBtn)

        ## cancel btn
        self.cancelBtn = QtGui.QPushButton("Cancel")
        self.cancelBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.cancelBtn, QtCore.SIGNAL('clicked()'),self.return_btn_callback)
        hboxLeft.addWidget(self.cancelBtn)

        ## view output
        self.outputBtn = QtGui.QPushButton("View Output")
        self.outputBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.outputBtn, QtCore.SIGNAL('clicked()'),self.view_output_btn_callback)
        hboxLeft.addWidget(self.outputBtn)

        ## info btn
        self.infoBtn = QtGui.QPushButton("Info")
        self.infoBtn.setMaximumWidth(self.buttonSize)
        self.connect(self.infoBtn, QtCore.SIGNAL('clicked()'),self.info_btn_callback)
        hboxLeft.addWidget(self.infoBtn)

        # compile selector
        rsBox = QtGui.QVBoxLayout()
        self.reportList = ['PDF','HTML']
        self.reportSelector = QtGui.QComboBox()
        for reportName in self.reportList:
            self.reportSelector.addItem(reportName)
        
        self.connect(self.reportSelector,QtCore.SIGNAL("activated(int)"),self.report_select_callback)
        #if self.mainWindow != None:
        #    reportDefault = self.mainWindow.controller.log.log['default_report']
        #    if self.reportList.__contains__(reportDefault):
        #        self.reportSelector.setCurrentIndex(self.reportList.index(reportDefault))

        rsBox.addWidget(self.reportSelector)
        hboxRight.addLayout(rsBox)

        # language selector
        lsBox = QtGui.QVBoxLayout()
        self.langList = ['R','Python']
        self.langSelector = QtGui.QComboBox()
        for langName in self.langList:
            self.langSelector.addItem(langName)
        
        self.connect(self.langSelector,QtCore.SIGNAL("activated(int)"),self.lang_select_callback)
        #self.connect(self.langSelector,QtCore.SIGNAL("curr(int)"),self.lang_select_callback)
        lsBox.addWidget(self.langSelector)
        hboxRight.addLayout(lsBox)

        ## finalize layout
        hbl.addLayout(vboxBottom)
        self.setLayout(hbl)
        self.use_welcome_mode()

    def hide_all(self):
        self.restoreDefaultsBtn.hide()
        self.saveBtn.hide()
        self.returnBtn.hide()
        self.cancelBtn.hide()
        self.loadBtn.hide()
        self.infoBtn.hide()
        self.compileCodeBtn.hide()
        self.compileReportBtn.hide()
        self.viewReportBtn.hide()
        self.langSelector.hide()
        self.reportSelector.hide()
        self.outputBtn.hide()
        self.mode = None

    def use_welcome_mode(self):
        self.hide_all()
        self.mode = 'welcome'

    def use_editor_mode(self):
        self.hide_all()
        self.compileCodeBtn.show()
        self.compileReportBtn.show()
        self.viewReportBtn.show()
        self.reportSelector.show()
        self.langSelector.show()
        self.mode = 'editor'

    def use_preferences_mode(self):
        self.hide_all()
        self.restoreDefaultsBtn.show()
        self.saveBtn.show()
        self.returnBtn.show()
        self.mode = 'preferences'

    def use_subprocess_mode(self):
        self.hide_all()
        self.cancelBtn.show()
        self.outputBtn.show()
        self.mode = 'subprocess'
        
    def use_sphinx_log_mode(self):
        self.hide_all()
        self.saveBtn.show()
        self.returnBtn.show()
        self.mode = 'sphinx-log'

    def use_new_project_mode(self):
        self.hide_all()
        self.cancelBtn.show()
        self.loadBtn.show()
        self.infoBtn.show()
        self.mode = 'new'

    def compile_code_btn_callback(self):
        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
        else:
            self.mainWindow.nga.build()
            goFlag = self.mainWindow.nga.goFlag

            #self.mainWindow.transitions.move_to_editor()
            #if goFlag == False:
            #    return
            #self.compile_report_btn_callback()
            #self.mainWindow.transitions.move_to_editor() 

    def compile_report_btn_callback(self):
        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
        else:
            selectedOutput = str(self.reportSelector.currentText())
            print selectedOutput
            if selectedOutput == 'PDF':
                self.mainWindow.nga.compile_pdf()
            elif selectedOutput == 'HTML':
                self.mainWindow.nga.compile_html()

            #self.mainWindow.transitions.move_to_editor() 

    def view_report_btn_callback(self):
        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
        else:
            selectedOutput = str(self.reportSelector.currentText())
            if selectedOutput == 'PDF':
                self.mainWindow.nga.view_pdf()
            elif selectedOutput == 'HTML':
                self.mainWindow.nga.view_html()

            self.mainWindow.transitions.move_to_editor() 

    def return_btn_callback(self):
        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
        else:
            if self.mode == 'subprocess':
                self.mainWindow.process.terminate()

            self.mainWindow.transitions.move_to_editor()

    def view_output_btn_callback(self):
        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
        else:
            self.mainWindow.transitions.view_output()

    def load_btn_callback(self):
        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
        else:
            selectedRow = self.mainWindow.newProject.get_selected()
            templatesDir = os.path.join(self.mainWindow.controller.baseDir,'templates')
            templatePath = os.path.join(templatesDir,selectedRow[0])
            self.mainWindow.ensure_tab_is_current()
            self.mainWindow.transitions.add_new_editor_tab(templatePath)
            self.mainWindow.transitions.move_to_editor()

    def report_select_callback(self):
        """
        changes the default report type when user toggles the checklist
        """

        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
            return
        
        selectedOutput = str(self.reportSelector.currentText())
        self.mainWindow.controller.log.log['default_report']  = selectedOutput
        self.mainWindow.controller.save()

    def lang_select_callback(self):
        """
        called after mainWindow.ensure_tab_is_current
        """

        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
            return
        
        selectedLanguage = str(self.langSelector.currentText())
        
        self.mainWindow.ensure_tab_is_current()
        currentIndex = self.mainWindow.controller.currentFileIndex
        currentLang  = self.mainWindow.controller.fileLangList[currentIndex]
        fileName = self.mainWindow.controller.fileNameList[currentIndex]

        if fileName == None:
            print 'WARNING: fileName in ButtonDock.lang_select_callback() is None'
            return

        self.mainWindow.controller.fileLangList[currentIndex] = selectedLanguage
        self.mainWindow.controller.save()

        ## ensure the current editor has the correct languages
        editor = self.mainWindow.controller.editorList[currentIndex]
        editor.lexer.language2 = selectedLanguage
        editor.lexer.set_languages()

        self.mainWindow.transitions.reload_tab(currentIndex)

    def info_btn_callback(self):
        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
            return

        QtGui.QMessageBox.about(self, "New file info",
                               """There are three file types that lpEdit can recognize:<p> 
<ul>
<li>reStructuredText <a href='http://docutils.sourceforge.net/rst.html'>(*.rst)</a></li><p>  
<li>Sweave <a href='http://leisch.userweb.mwn.de/Sweave'>(*.rnw)</a></li><p>
<li>noweb <a href='http://www.cs.tufts.edu/~nr/noweb'>(*.nw)</a></li> 
</ul>

<p>Both noweb and Sweave documents are essentially a mixture of LaTeX and code. 
Restructured text (reST) is a markup language capable of producing LaTeX.  
Sweave documents may contain only R code, whereas noweb or reST documents make 
use of other languages.<p> 

No matter which document type you choose the code is included in the documents 
in exactly the same manner.""")


    def restore_defaults_btn_callback(self):
        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
        else:
            print 'restoring defaults.'

        self.mainWindow.preferences.restore_defaults_callback()

    def save_btn_callback(self):
        if self.mainWindow == None:
            print 'function does nothing without mainWindow present'
        else:
            print 'saving all...'

            if self.mode == 'sphinx-log':
                fileIndex = self.mainWindow.controller.currentFileIndex
                fileName = self.mainWindow.controller.fileNameList[fileIndex]
                filePath = self.mainWindow.controller.filePathList[fileIndex]
                sphinxLogPath = os.path.join(os.path.split(filePath)[0],'_sphinx','sphinx.log')
                sphinxLogUI = self.mainWindow.sphinxLogs[sphinxLogPath]
                sphinxLogUI.save_callback()

            elif self.mode == 'preferences':
                self.mainWindow.preferences.save_callback()

    def generic_callback(self):
        print 'generic callback'

### Run the tests
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    bdock = ButtonDock()
    bdock.show()
    sys.exit(app.exec_())
