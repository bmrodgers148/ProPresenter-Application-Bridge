"Propresenter Application Bridge"
"The purpose of this program is to provide a framework to interface other applications with propresenter using slide notes"

import os
import json
from ProPresenterCommModule import ProPresenterStageDisplayClientComms
import time
import midiProcess
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import rtmidi

class ProData():

    def __init__(self, master = None):


        self.prevNote = ''
        self.connectStatus = 'Disconnected'
        self.noteLog = []
        try:
            ConfigData_Filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
            ConfigData_JSON = open(ConfigData_Filename).read()
            ConfigData = json.loads(ConfigData_JSON)
            self.ProP_IPAddress = ConfigData['IPAddress']
            self.ProP_IPPort = int(ConfigData['IPPort'])
            self.ProP_Password = ConfigData['Password']
            self.MSCCmdFormat = ConfigData['MSCCmdFormat']
            self.MSCDeviceID = ConfigData['MSCDeviceID']
            self.StopRepeats = ConfigData['StopRepeats']
            self.midiPort = int(ConfigData['midiPort'])

        except Exception as e:
            print("EXCEPTION: Cannot load and parse Config.JSON File: ")
            print(e)
        self.setupUi(MainWindow)
        self.connect()
        self.reconnect_tick()

    def connect(self):
        # Connect to ProPresenter and setup the necessary callbacks
        self.tryReconnect = True
        self.disconnectTime = 0

        self.ProPresenter = ProPresenterStageDisplayClientComms(self.ProP_IPAddress, self.ProP_IPPort, self.ProP_Password)
        self.ProPresenter.addSubscription("Connected", self.connected)
        self.ProPresenter.addSubscription("ConnectionFailed", self.connectFailed)
        self.ProPresenter.addSubscription("Disconnected", self.disconnected)
        self.ProPresenter.addSubscription("CurrentSlideNotes",self.updateSlideNotesCurrent)
        self.ProPresenter.daemon = True
        self.ProPresenter.start()
        midiProcess.openPort(self.midiPort)

    def connected(self, data):
        self.connectStatus = "ProPresenter Connected"
        self.retranslateUi(MainWindow)

    def connectFailed(self, error):
        self.tryReconnect = True
        
        if self.disconnectTime == 0:
            self.disconnectTime = time.time()
        
        self.connectStatus = 'ProPresenter Connect Failed'
        self.retranslateUi(MainWindow)
    
    def disconnected(self, error):
        self.tryReconnect = True
        
        if self.disconnectTime == 0:
            self.disconnectTime = time.time()
        
        self.connectStatus = "ProPresenter Disconnected"
        self.retranslateUi(MainWindow)

    def reconnect_tick(self):
        if self.tryReconnect and self.disconnectTime < time.time() - 5:
            self.connectStatus = "Attempting to reconnect to ProPresenter"
            self.retranslateUi(MainWindow)
            self.connect()
        

    def updateSlideNotesCurrent(self, data):
        if data['text'] is not None:
            self.currentNote = str(data['text'])
            if self.StopRepeats: 
                if self.currentNote != self.prevNote:
                    midiProcess.processAndSend(self.currentNote, self.MSCDeviceID, self.MSCCmdFormat)
                    self.prevNote = self.currentNote
                    if (len(self.noteLog) >= 5):
                        self.noteLog.pop(0)
                    self.noteLog.append(self.currentNote)
                    self.listWidget.clear()
                    self.listWidget.addItems(self.noteLog)
                    
            else:
                midiProcess.processAndSend(self.currentNote, self.MSCDeviceID, self.MSCCmdFormat)
                if (len(self.noteLog) >= 5):
                    self.noteLog.pop(0)
                self.noteLog.append(self.currentNote)
                self.listWidget.clear()
                self.listWidget.addItems(self.noteLog)


        else:
            self.currentNote = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(781, 574)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 351, 511))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_5)
        self.label_6 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.midiPortSelect = QtWidgets.QComboBox(self.widget)
        self.midiPortSelect.setObjectName("midiPortSelect")
        self.midiPortSelect.addItems(midiProcess.available_ports)
        self.midiPortSelect.setCurrentIndex(self.midiPort)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.midiPortSelect)
        self.label_7 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.cmdFormatEntry = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cmdFormatEntry.setFont(font)
        self.cmdFormatEntry.setText(self.MSCCmdFormat)
        self.cmdFormatEntry.setObjectName("cmdFormatEntry")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cmdFormatEntry)
        self.label_8 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.DeviceIDEntry = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.DeviceIDEntry.setFont(font)
        self.DeviceIDEntry.setText(self.MSCDeviceID)
        self.DeviceIDEntry.setObjectName("DeviceIDEntry")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.DeviceIDEntry)
        self.gridLayout.addLayout(self.formLayout, 5, 0, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 7, 0, 1, 2)
        self.stopRepeatCheck = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.stopRepeatCheck.setFont(font)
        self.stopRepeatCheck.setChecked(self.StopRepeats)
        self.stopRepeatCheck.setObjectName("stopRepeatCheck")
        self.gridLayout.addWidget(self.stopRepeatCheck, 8, 0, 1, 2, QtCore.Qt.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 9, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.ipEntry = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ipEntry.setFont(font)
        self.ipEntry.setText(self.ProP_IPAddress)
        self.ipEntry.setObjectName("ipEntry")
        self.gridLayout.addWidget(self.ipEntry, 1, 1, 1, 1)
        self.portEntry = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.portEntry.setFont(font)
        self.portEntry.setText(str(self.ProP_IPPort))
        self.portEntry.setObjectName("portEntry")
        self.gridLayout.addWidget(self.portEntry, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.passwordEntry = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passwordEntry.setFont(font)
        self.passwordEntry.setText(self.ProP_Password)
        self.passwordEntry.setObjectName("passwordEntry")
        self.gridLayout.addWidget(self.passwordEntry, 3, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.saveProSettingsBtn = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.saveProSettingsBtn.setFont(font)
        self.saveProSettingsBtn.setObjectName("saveProSettingsBtn")
        self.gridLayout.addWidget(self.saveProSettingsBtn, 10, 0, 1, 2)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(400, 10, 47, 14))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.connectionStatus = QtWidgets.QLabel(self.centralwidget)
        self.connectionStatus.setGeometry(QtCore.QRect(460, 10, 271, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.connectionStatus.setFont(font)
        self.connectionStatus.setObjectName("connectionStatus")
        self.midiStatus = QtWidgets.QLabel(self.centralwidget)
        self.midiStatus.setGeometry(QtCore.QRect(460, 30, 271, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.midiStatus.setFont(font)
        self.midiStatus.setObjectName("midiStatus")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(400, 130, 256, 131))
        self.listWidget.setObjectName("listWidget")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(400, 110, 251, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setGeometry(QtCore.QRect(450, 310, 131, 23))
        self.quitButton.setObjectName("quitButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.saveProSettingsBtn.clicked.connect(self.saveAndConnect)
        #self.quitButton.clicked.connect(self.quitProgram)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "MIDI Settings"))
        self.label_6.setText(_translate("MainWindow", "Port:"))
        self.label_7.setText(_translate("MainWindow", "Command Format: "))
        self.label_8.setText(_translate("MainWindow", "Device ID:"))
        self.label_9.setText(_translate("MainWindow", "Miscellaneous Settings"))
        self.stopRepeatCheck.setText(_translate("MainWindow", "Prevent Repeat Messages"))
        self.label_2.setText(_translate("MainWindow", "IP Address:"))
        self.label_4.setText(_translate("MainWindow", "Password:"))
        self.label_3.setText(_translate("MainWindow", "Port:"))
        self.label.setText(_translate("MainWindow", "ProPresenter Connection Settings"))
        self.saveProSettingsBtn.setText(_translate("MainWindow", "Save and Reconnect"))
        self.label_10.setText(_translate("MainWindow", "Status:"))
        self.connectionStatus.setText(_translate("MainWindow", str(self.connectStatus)))
        if midiProcess.midiout.is_port_open:
            self.midiStatus.setText(_translate("MainWindow", "MIDI Port Open"))
        else:
            self.midiStatus.setText(_translate("MainWindow", "MIDI Port Closed"))
        self.label_11.setText(_translate("MainWindow", "Recent Messages"))
        self.quitButton.setText(_translate("MainWindow", "Quit"))
        self.quitButton.clicked.connect(self.quitProgram)

    def saveAndConnect(self):
        self.ProP_IPAddress = self.ipEntry.text()
        self.ProP_IPPort = int(self.portEntry.text())
        self.ProP_Password = self.passwordEntry.text()
        self.MSCCmdFormat = self.cmdFormatEntry.text()
        self.MSCDeviceID = self.DeviceIDEntry.text()
        self.StopRepeats = self.stopRepeatCheck.isChecked()
        self.midiPort = self.midiPortSelect.currentIndex()

        ConfigData_Filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.json")
        ConfigData_JSON = open(ConfigData_Filename).read()
        ConfigData = json.loads(ConfigData_JSON)  
        ConfigData['IPAddress'] =  self.ProP_IPAddress
        ConfigData['IPPort'] = self.ProP_IPPort
        ConfigData['Password'] = self.ProP_Password
        ConfigData['MSCCmdFormat'] = self.MSCCmdFormat
        ConfigData['MSCDeviceID'] = self.MSCDeviceID
        ConfigData['StopRepeats'] = self.StopRepeats
        ConfigData['midiPort'] = self.midiPort
        ConfigData_JSON = open(ConfigData_Filename, 'w')
        json.dump(ConfigData, ConfigData_JSON, indent=1)


        self.connect()
    def quitProgram(self):
        
        self.ProPresenter.stop()
        time.sleep(0.5)
        exit()

#pro = ProData()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    pro = ProData()
    MainWindow.show()
    sys.exit(app.exec_())

























