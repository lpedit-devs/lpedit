import sys,os,math
from PyQt4 import QtGui
from PyQt4 import QtCore

class Tooltip(QtGui.QWidget):
    def __init__(self, msg='This is a tooltip', parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setToolTip(msg)
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))

class Waiting(QtGui.QWidget):
    def __init__(self, parent = None):

        QtGui.QWidget.__init__(self, parent)
        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, QtCore.Qt.transparent)
        self.setPalette(palette)

    def paintEvent(self, event):

        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(QtGui.QColor(255, 255, 255, 127)))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        for i in range(6):
            if (self.counter / 5) % 6 == i:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(127 + (self.counter % 5)*32, 127, 127)))
            else:
                painter.setBrush(QtGui.QBrush(QtGui.QColor(127, 127, 127)))
            painter.drawEllipse(
                self.width()/2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
                self.height()/2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10,
                20, 20)

            painter.end()

    def showEvent(self, event):
        self.timer = self.startTimer(50)
        self.counter = 0

    def timerEvent(self, event):
        self.counter += 1
        self.update()
        if self.counter == 60:
            self.killTimer(self.timer)
            self.hide()

class RadioBtnWidget(QtGui.QWidget):

    def __init__(self,btnLabels,parent=None,default=None,callbackFn=None,color='white',widgetLabel=None,vertical=False):
        QtGui.QWidget.__init__(self,parent)

        if default != None and btnLabels.__contains__(default) == False:
            print "ERROR: RadioBtnWidget - bad default specified",default 
            return None

        if vertical == False:
            btnBox = QtGui.QVBoxLayout()
        else:
            btnBox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()
        hbox1 = QtGui.QHBoxLayout()
        hbox2 = QtGui.QHBoxLayout()
        if widgetLabel != None:
            self.widgetLabel = QtGui.QLabel(widgetLabel)
            hbox1.addWidget(self.widgetLabel) 

        self.selectedItem = None
        self.btnLabels = btnLabels
        self.btns = {}
        self.btnGroup = QtGui.QButtonGroup(parent)
        self.color = color

        for bLabel in self.btnLabels:
            rad = QtGui.QRadioButton(bLabel)
            self.btns[bLabel] = rad
            self.connect(self.btns[bLabel], QtCore.SIGNAL('clicked()'),lambda item=bLabel:self.set_selected(item))
            btnBox.addWidget(self.btns[bLabel])

            if callbackFn != None:
                #self.connect(self.btns[bLabel], QtCore.SIGNAL('clicked()'),lambda item=bLabel:callbackFn(item=item))
                self.connect(self.btns[bLabel], QtCore.SIGNAL('clicked()'),callbackFn)

            if default != None and bLabel == default:
                self.btns[bLabel].setChecked(True)
                self.selectedItem = bLabel

        vbox.addLayout(hbox1)
        hbox2.addLayout(btnBox)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

    def set_selected(self,item=None):
        if item !=None:
            self.selectedItem = item

class Slider(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle('Slider')
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider.setFocusPolicy(QtCore.Qt.NoFocus)
        #self.slider.setGeometry(30, 40, 100, 30)
       
class Imager(QtGui.QWidget):
    def __init__(self, imgPath, parent=None):
        QtGui.QWidget.__init__(self, parent)

        hbox = QtGui.QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignCenter)
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignCenter)

        if os.path.exists(imgPath) == False:
            print "WARNING: Imager -- image path specified does not exist"

        pixmap = QtGui.QPixmap(imgPath)
        label = QtGui.QLabel(self)
        label.setPixmap(pixmap)

        hbox.addWidget(label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

class Tooltip(QtGui.QWidget):
    def __init__(self, msg='This is a tooltip', parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setToolTip(msg)
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))

class ProgressBar(QtGui.QWidget):
    def __init__(self,parent=None,buttonLabel='Cancel',label=None):
        QtGui.QWidget.__init__(self)

        self.running = False 
        vbl = QtGui.QVBoxLayout() 
        hbl1 = QtGui.QHBoxLayout() 
        hbl1.setAlignment(QtCore.Qt.AlignCenter)
        hbl2 = QtGui.QHBoxLayout()
        hbl2.setAlignment(QtCore.Qt.AlignCenter) 
        hbl3 = QtGui.QHBoxLayout()
        hbl3.setAlignment(QtCore.Qt.AlignLeft) 

        self.progressLabel = QtGui.QLabel(str(label)) 
        hbl3.addWidget(self.progressLabel)
        if label == None:
            self.progressLabel.hide()
    
        self.pbar = QtGui.QProgressBar(self) 
        hbl1.addWidget(self.pbar)

        if buttonLabel != None:
            self.button = QtGui.QPushButton(buttonLabel, self)
            self.button.setMaximumWidth(150)
            self.button.setMinimumWidth(150)
            self.button.setFocusPolicy(QtCore.Qt.NoFocus)
            hbl2.addWidget(self.button)
        else: 
            self.button = None

        self.setLayout(vbl) 
        self.timer = QtCore.QBasicTimer()
        self.step = 0;

        ## finalize layout
        vbl.addLayout(hbl1)
        vbl.addLayout(hbl2)
        vbl.addLayout(hbl3)

    def set_label(self,label):
        self.progressLabel.setText(label)
        self.progressLabel.setStyleSheet("font: 7pt")
        self.progressLabel.show()
    
    #def onStart(self): 
    #    if self.running == False: 
    #        if self.button != None: 
    #            self.button.setText('Please wait...')
    #            self.button.setEnabled(False)
    #            QtCore.QCoreApplication.processEvents()
    #
    #    self.running = True
            
    def move_bar(self,step): 
        self.step = step
        self.pbar.setValue(self.step) 
        self.show()
        QtCore.QCoreApplication.processEvents()

    def set_callback(self,callback):
        self.connect(self.button,QtCore.SIGNAL('clicked()'),callback)
