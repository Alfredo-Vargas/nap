import sys
import NapMethods
from PyQt5 import QtSvg
from PyQt5.QtWidgets import (
	QApplication, QGraphicsItem, QLabel, QWidget,
	QHBoxLayout, QVBoxLayout, 
	QLineEdit, QFileDialog, QPushButton, QCheckBox, QGraphicsScene, QGraphicsView)

##########################################################################################
#                   https://realpython.com/python-pyqt-layout/                           #
##########################################################################################
class NapMainWindow(QWidget):
	def __init__(self):		# constructor
		super().__init__()	# shoud inherit all from the class NapMainWindow
		self.setWindowTitle("NAP: Network Analyzer with Python")
		# Create an outer layout
		outerLayout = QVBoxLayout()
		## Create a form layout for the file path field, load pcap button and capture live button
		topLayout = QHBoxLayout()

		self.pathToFile = QLineEdit('', self)	# you want to modify this property that is why becomes a public attribute
		topLayout.addWidget(self.pathToFile, 2)

		btnLoadPcapFile = QPushButton('Load PCAP File', self)
		btnLoadPcapFile.clicked.connect(self.browse_files)
		topLayout.addWidget(btnLoadPcapFile, 1)

		topLayout.addWidget(QPushButton("Capture-Live"), 1)

		## Create the body layout  (graphviz and options will be placed there)
		bodyLayout = QHBoxLayout()

		### Graphics layout
		graphicsLayout = QVBoxLayout()

		graphicsLayout.addWidget(QCheckBox("Show Traffic Size in Bytes: "))

		self.graphicOutput = QGraphicsView()	# public attribute because we need to change the conversation images
		self.scene = QGraphicsScene()
		#graphicView = QGraphicsView(self.scene, self)
		graphicsLayout.addWidget(self.graphicOutput)

		### Legend layout
		legendLayout = QVBoxLayout()
		legendLayout.addWidget(QLabel("Legend"))

		### Options layout
		optionsLayout = QVBoxLayout()

		btnShowIPConversation = QPushButton("IP\nConversation", self)
		btnShowIPConversation.clicked.connect(self.show_ip_conversation)
		optionsLayout.addWidget(btnShowIPConversation)

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
	
		# Here we define the actions/methods/functions:

	def browse_files(self):
		response = QFileDialog.getOpenFileName(self, 'Open File', '.', 'PCAP files (*.pcap)')
		self.pathToFile.setText(response[0])
		NapMethods.generate_conversations(response[0])
	
	# def createGraphicView(self):
	# 	self.graphicOutput.scene = QGraphicsScene()
	# 	graphicView = QGraphicsView(self.graphicOutput.scene, self)

	##########################################################################################
	#  https://doc.qt.io/archives/qtforpython-5.12/PySide2/QtSvg/QGraphicsSvgItem.html       #
	##########################################################################################
	def show_ip_conversation(self, path ="./conversations/ip_conversation_twopi.gv.svg"):
		ipv4Conversation = QtSvg.QGraphicsSvgItem("./conversations/ip_conversation_twopi.gv.svg")
		self.graphicOutput.showNormal(ipv4Conversation)
		# ipConversation = QtSvg.QSvgRenderer("./conversations/ip_conversation_twopi.gv.svg")
		# graphicView = QGraphicsView(self.graphicOutput.scene, self)
		# graphicView.setGeometry(0,0, 600, 500)


def runNap():
	app = QApplication(sys.argv)
	win = NapMainWindow()
	win.show()
	sys.exit(app.exec_())

runNap()
