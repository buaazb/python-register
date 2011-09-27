# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Tue Sep 27 14:12:23 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1233, 624)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QtCore.QSize(400, 0))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        
        self.widget = MyDynamicMplCanvas(self.splitter)
      
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(1000, 600))
        self.widget.setObjectName(_fromUtf8("widget"))
        
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setContentsMargins(-1, 6, -1, -1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Fittings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.listWidget = QtGui.QListWidget(self.layoutWidget)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout.addWidget(self.splitter)
        
#        
#        self.listWidget.connect(
#            self.listWidget, 
#            QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), 
#            self.mouseSlot
#            )
#        
#        self.listWidget.connect(
#            self.listWidget, 
#            QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), 
#            self.mouseSlot
#            )
#        
#        self.listWidget.connect(
#            self.listWidget, 
#            QtCore.SIGNAL("itemActivated(QListWidgetItem*)"), 
#            self.mouseSlot
#            )
#
        self.listWidget.connect(
            self.listWidget, 
            QtCore.SIGNAL("currentItemChanged (QListWidgetItem *,QListWidgetItem *)"), 
            self.itemChangedSlot)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def itemChangedSlot(self, item, item2):
        self.widget.formPlot(self.searchMap[item].warpedImage)
        
    def updateList(self, search):
        """
        Takes the search datastructure and makes a list of it.
        """
        
        self.searchMap = {}
        
        for index, step in enumerate(search):
            item = QtGui.QListWidgetItem(self.listWidget)
            item.setText(
                "itteration: {}, error: {}".format(
                    index,
                    step.error
                    )
                )
            self.searchMap[item] = step
            
    def retranslateUi(self, Dialog):
        pass

###############################################################################
# MPL widget 
###############################################################################
import plot

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, image=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        
        if image is not None:
            self.formPlot(image)
            
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def formPlot(self, image):
        self.axes.imshow(
            image, 
            #origin='lower', 
            interpolation='nearest',
            cmap='gray'
            )
        self.draw()