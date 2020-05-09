import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QToolTip, QMessageBox, QLabel, QDialog,QGroupBox, QVBoxLayout, QGridLayout, QComboBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import configparser, os.path

import serialList

config = configparser.ConfigParser()
if(os.path.exists('config.ini')):
    config.read('config.ini')
else:
    config['serial'] = {}

class Window2(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Configuration"
        self.width = 300
        self.height = 500
        self.left = windowpos[0]+(windowpos[2]-self.width)/2
        self.top = windowpos[1]+100
        
        global window2pos
        window2pos = [self.frameGeometry().top(), self.frameGeometry().left(), self.frameGeometry().width(), self.frameGeometry().height()]
        
        self.main_window()
    def main_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top, self.width, self.height)
        self.createGridLayout()
        
        windowLayout2 = QVBoxLayout()
        windowLayout2.addWidget(self.horizontalGroupBox2)
        self.setLayout(windowLayout2)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox2 = QGroupBox("Serial Settings")
        layout2 = QGridLayout()

        self.label1 = QLabel("Baudrate", self)
        layout2.addWidget(self.label1,0,0)
        
        self.comboBox1 = QComboBox(self)
        self.baud = ["300", "600", "2400", "4800", "9600", "14400", "19200", "28800", "38400", "57600", "115200"]
        self.comboBox1.addItems(self.baud)
        if(os.path.exists('config.ini')):
            self.comboBox1.setCurrentIndex(self.baud.index(config['serial']['baud_rate']))
        layout2.addWidget(self.comboBox1,0,1)
        
        self.label2 = QLabel("Port", self)
        layout2.addWidget(self.label2,1,0)

        self.comboBox2 = QComboBox(self)
        self.port = serialList.serial_ports()[::-1]
        if(self.port == "[]"): 
            print("Vazio")
        print(self.port)
        self.comboBox2.addItems(self.port)
        if(os.path.exists('config.ini')):
            self.comboBox2.setCurrentIndex(self.port.index(config['serial']['port']))
        layout2.addWidget(self.comboBox2,1,1)
        
        self.label3 = QLabel("Manager", self)
        layout2.addWidget(self.label3,2,0)

        self.pushButton1 = QPushButton("Cancel", self)
        self.pushButton1.setToolTip("Exit without saving")
        self.pushButton1.clicked.connect(self.closeWindow2)
        layout2.addWidget(self.pushButton1,3,0)

        self.pushButton1 = QPushButton("Apply", self)
        self.pushButton1.setToolTip("Save data")
        self.pushButton1.clicked.connect(self.Apply)
        layout2.addWidget(self.pushButton1,3,1)

        self.horizontalGroupBox2.setLayout(layout2)
    
    def closeWindow2(self):
        self.close()
    def window2Pos(self):
        print("oi")
        #print(self.geometry())
    def Apply(self):
        config['serial']['baud_rate'] = self.comboBox1.currentText()
        config['serial']['port'] = self.comboBox2.currentText()
        self.close()
        with open('config.ini', 'w+') as configfile:    # save
            config.write(configfile)

class Window(QDialog):
    def __init__(self):
        super().__init__()

        self.title = "Telemetry"
        self.top = 200
        self.left = 1920/2
        self.width = 800
        self.height = 640
        
        self.main_window()

    def main_window(self):
        #self.label = QLabel("Manager", self)
        #self.label.move(285, 175)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top, self.width, self.height)

        self.createGridLayout()
        windowLayout1 = QVBoxLayout()
        #windowLayout1.addWidget(self.horizontalGroupBox1)
        self.setLayout(windowLayout1)
        self.show()

    def createGridLayout(self):
        #self.horizontalGroupBox1 = QGroupBox("Serial Settings")
        layout1 = QGridLayout()

        self.label1 = QLabel("Baudrate", self)
        layout1.addWidget(self.label1,0,0)

        self.pushButton = QPushButton("Config", self)
        #self.pushButton.move(0, 0)
        self.pushButton.setToolTip("<h3>Start the Session</h3>")
        self.pushButton.clicked.connect(self.window2)              # <===
        layout1.addWidget(self.pushButton,0,0)

        #self.horizontalGroupBox1.setLayout(layout1)

    def window2(self):                                             # <===
        global windowpos
        windowpos = [self.frameGeometry().left(), self.frameGeometry().top(), self.frameGeometry().width(), self.frameGeometry().height()]
        self.w = Window2()
        self.w.show()
        #self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())