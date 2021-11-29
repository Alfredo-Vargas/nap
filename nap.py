from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(877, 654)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnShowIPConversation = QtWidgets.QPushButton(self.centralwidget)
        self.btnShowIPConversation.setGeometry(QtCore.QRect(790, 90, 81, 41))
        self.btnShowIPConversation.setObjectName("btnShowIPConversation")
        self.btnShowEthernetConversation = QtWidgets.QPushButton(self.centralwidget)
        self.btnShowEthernetConversation.setGeometry(QtCore.QRect(790, 40, 80, 41))
        self.btnShowEthernetConversation.setObjectName("btnShowEthernetConversation")
        self.pathToFile = QtWidgets.QLineEdit(self.centralwidget)
        self.pathToFile.setGeometry(QtCore.QRect(10, 10, 451, 21))
        self.pathToFile.setText("")
        self.pathToFile.setObjectName("pathToFile")
        self.btnLoadPcapFile = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoadPcapFile.setGeometry(QtCore.QRect(470, 10, 121, 21))
        self.btnLoadPcapFile.setObjectName("btnLoadPcapFile")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 40, 761, 571))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 877, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_PCAP_File = QtWidgets.QAction(MainWindow)
        self.actionLoad_PCAP_File.setCheckable(False)
        self.actionLoad_PCAP_File.setObjectName("actionLoad_PCAP_File")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionLoad_PCAP_File)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NAP - Network Analyzer with Python"))
        self.btnShowIPConversation.setText(_translate("MainWindow", "Show IPv4\n""Conversation"))
        self.btnShowEthernetConversation.setText(_translate("MainWindow", "Show Ethernet\n"" Conversation"))
        self.btnLoadPcapFile.setText(_translate("MainWindow", "Load PCAP File"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionLoad_PCAP_File.setText(_translate("MainWindow", "Load PCAP File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
