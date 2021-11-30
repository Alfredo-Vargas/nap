import sys
from PyQt5.QtWidgets import (
	QApplication, QLabel, QWidget,
	QHBoxLayout, QVBoxLayout, QFormLayout,
	QLineEdit, QPushButton, QCheckBox, QGraphicsView)

##########################################################################################
#                   https://realpython.com/python-pyqt-layout/
##########################################################################################
class NapMainWindow(QWidget):
	def __init__(self):		# constructor
		super().__init__()	# shoud inherit all from the class NapMainWindow
		self.setWindowTitle("NAP: Network Analyzer with Python")
		# Create an outer layout
		outerLayout = QVBoxLayout()
		## Create a form layout for the file path field, load pcap button and capture live button
		topLayout = QHBoxLayout()
		topLayout.addWidget(QLineEdit(""), 2)
		topLayout.addWidget(QPushButton("Load PCAP File"), 1)
		topLayout.addWidget(QPushButton("Capture-Live"), 1)
		## Create the body layout  (graphviz and options will be placed there)
		bodyLayout = QHBoxLayout()
		### Graphics layout
		graphicsLayout = QVBoxLayout()
		graphicsLayout.addWidget(QCheckBox("Show Traffic Size in Bytes: "))
		graphicsLayout.addWidget(QGraphicsView())
		### Legend layout
		legendLayout = QVBoxLayout()
		legendLayout.addWidget(QLabel("Legend"))
		### Options layout
		optionsLayout = QVBoxLayout()
		optionsLayout.addWidget(QPushButton("IP\nConversation"))
		optionsLayout.addWidget(QPushButton("Ethernet\nConversation"))
		optionsLayout.addWidget(QCheckBox("dot"))
		optionsLayout.addWidget(QCheckBox("twopi"))
		optionsLayout.addWidget(QCheckBox("neato"))
		optionsLayout.addWidget(QCheckBox("circo"))
		self.setGeometry(500,500, 1600, 900)

		# We assemble the body layout
		bodyLayout.addLayout(graphicsLayout)
		bodyLayout.addLayout(legendLayout)
		bodyLayout.addLayout(optionsLayout)

		# We assemble the outer layout
		outerLayout.addLayout(topLayout)
		outerLayout.addLayout(bodyLayout)

		self.setLayout(outerLayout)
	
		#self.btnLoadPcapFile = QPushButton('Load PCAP File', self)
		#self.btnLoadPcapFile.resize(200, 64)
		#self.btnLoadPcapFile.move(1200, 50)

        # self.pathToFile.setGeometry(QtCore.QRect(10, 10, 451, 21))
        # self.pathToFile.setText("")
        # self.pathToFile.setObjectName("pathToFile")
        # self.btnLoadPcapFile = QtWidgets.QPushButton(self.centralwidget)
        # self.btnLoadPcapFile.setGeometry(QtCore.QRect(470, 10, 121, 21))
        # self.btnLoadPcapFile.setObjectName("btnLoadPcapFile")

def runNap():
	app = QApplication(sys.argv)
	win = NapMainWindow()
	win.show()
	sys.exit(app.exec_())

runNap()
