# TODO PORT MIRRORING FOR USE IN SWITCHES AND ROUTERS FOR LIVE - CAPTURE FOR INSTANCE
# TODO Migrate to browser for display of the figures and filtering of options
##########################################################################################
#                   https://realpython.com/python-pyqt-layout/                           #
#  https://doc.qt.io/archives/qtforpython-5.12/PySide2/QtSvg/QGraphicsSvgItem.html       #
##########################################################################################
import sys
import NapMethods
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtWidgets import (
    QApplication, QLabel, QRadioButton, QWidget,
    QHBoxLayout, QVBoxLayout,
    QLineEdit, QFileDialog, QPushButton, QCheckBox, QGraphicsScene, QGraphicsView)

class NapMainWindow(QWidget):


    def __init__(self):		# constructor
        super().__init__()	# shoud inherit all from the class NapMainWindow
        self.setWindowTitle("NAP: Network Analyzer with Python")
        napMode = "off"
        self.napMode = napMode # possible values, ip, mac, ...)
        #  Create an outer layout
        outerLayout = QVBoxLayout()
        #  Create a form layout for the file path field, load pcap button and capture live button
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

        btnGenerateConversations = QPushButton('Generate Conversations', self)
        btnGenerateConversations.clicked.connect(self.generate_conversations)
        graphicsLayout.addWidget(btnGenerateConversations, 1)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        graphicsLayout.addWidget(self.view)

        ### Legend layout
        legendLayout = QVBoxLayout()
        legendLayout.addWidget(QLabel("Legend"))

        ### Options layout
        optionsLayout = QVBoxLayout()

        btnShowIPConversation = QPushButton("IP\nConversation", self)
        optionsLayout.addWidget(btnShowIPConversation)

        btnShowEthernetConversation = QPushButton("Ethernet\nConversation", self)
        optionsLayout.addWidget(btnShowEthernetConversation)

        self.radioTwopi = QRadioButton("twopi")
        optionsLayout.addWidget(self.radioTwopi)
        self.radioDot = QRadioButton("dot")
        optionsLayout.addWidget(self.radioDot)
        self.radioNeato = QRadioButton("neato")
        optionsLayout.addWidget(self.radioNeato)
        self.radioCirco = QRadioButton("circo")
        optionsLayout.addWidget(self.radioCirco)

        # We assemble the body layout
        bodyLayout.addLayout(graphicsLayout)
        bodyLayout.addLayout(legendLayout)
        bodyLayout.addLayout(optionsLayout)

        # We assemble the outer layout
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(bodyLayout)

        self.setGeometry(500,500, 1600, 900)
        self.setLayout(outerLayout)
    
        # Here are the Method Calls (place it after all attributes have been declared)
        btnShowEthernetConversation.clicked.connect(lambda: self.show_conversation("ether"))
        btnShowIPConversation.clicked.connect(lambda: self.show_conversation("ip"))
        self.radioTwopi.clicked.connect(lambda: self.show_conversation(self.napMode))
        self.radioDot.clicked.connect(lambda: self.show_conversation(self.napMode))
        self.radioNeato.clicked.connect(lambda: self.show_conversation(self.napMode))
        self.radioCirco.clicked.connect(lambda: self.show_conversation(self.napMode))

        # Here we define the actions/methods/functions:
    def browse_files(self):
        response = QFileDialog.getOpenFileName(self, 'Open File', '.', 'PCAP files (*.pcap)')
        if response[0] != "":	# to avoid crashing if the user cancels
            self.pathToFile.setText(response[0])
    def generate_conversations(self):
        pcap_file = self.pathToFile.text()
        NapMethods.generate_conversations(pcap_file)
    
    def show_conversation(self, mode = "off"):
        self.napMode = mode # we update the mode of the just pressed button
        if (mode == "ip"):
            twopi_figure = "./conversations/ip_conversation_twopi.gv.svg"
            dot_figure = "./conversations/ip_conversation_dot.gv.svg"
            neato_figure = "./conversations/ip_conversation_neato.gv.svg"
            circo_figure = "./conversations/ip_conversation_circo.gv.svg"
        elif (mode == "ether"):
            twopi_figure = "./conversations/ethernet_conversation_twopi.gv.svg"
            dot_figure = "./conversations/ethernet_conversation_dot.gv.svg"
            neato_figure = "./conversations/ethernet_conversation_neato.gv.svg"
            circo_figure = "./conversations/ethernet_conversation_circo.gv.svg"
        if (self.napMode != "off"):		# IS NOT DETECTING WHETHER OR NOT YOU LOADED THE PCAP FILE
            # 0.x the percentage (x0% of the QGraphicsView, 768 rendered width pixels of the svg images)
            scale_factor = 0.7 * self.view.width() / 768
            if (not self.radioTwopi.isChecked() and not self.radioDot.isChecked() 
                and not self.radioNeato.isChecked() and not self.radioCirco.isChecked()):
                svg_twopi = QGraphicsSvgItem(twopi_figure)
                self.scene.addItem(svg_twopi)
                svg_twopi.setScale(scale_factor)
                self.radioTwopi.toggle()
            else:
                if (self.radioTwopi.isChecked()):
                    self.scene.clear()
                    svg_twopi = QGraphicsSvgItem(twopi_figure)
                    self.scene.addItem(svg_twopi)
                    svg_twopi.setScale(scale_factor)
                    self.radioTwopi.toggle()
                elif (self.radioDot.isChecked()):
                    self.scene.clear()
                    svg_dot = QGraphicsSvgItem(dot_figure)
                    self.scene.addItem(svg_dot)
                    svg_dot.setScale(scale_factor)
                    self.radioDot.toggle()
                elif (self.radioNeato.isChecked()):
                    self.scene.clear()
                    svg_neato = QGraphicsSvgItem(neato_figure)
                    self.scene.addItem(svg_neato)
                    svg_neato.setScale(scale_factor)
                    self.radioNeato.toggle()
                elif (self.radioCirco.isChecked()):
                    self.scene.clear()
                    svg_circo = QGraphicsSvgItem(circo_figure)  
                    self.scene.addItem(svg_circo)
                    svg_circo.setScale(scale_factor)
                    self.radioCirco.toggle()

def runNap():
    app = QApplication(sys.argv)
    win = NapMainWindow()
    win.show()
    sys.exit(app.exec_())

runNap()
