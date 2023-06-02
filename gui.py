import sys
import threading

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, \
    QPushButton, QComboBox, QLineEdit, \
        QMessageBox
from PyQt5 import uic
from PyQt5.Qt import QIntValidator

from utils import SyncClipboard


class Worker(QObject):
    updateStatusLabel = pyqtSignal(str)
    showMsg = pyqtSignal(str, bool)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.syncclipboard = SyncClipboard(print_msg=self.print_msg)


    def start_server(self, port):
        try:
            self.syncclipboard.start_server(port)
        except Exception as e:
            self.showMsg.emit(f"An error occured while running the server: {e}", True)

        self.finished.emit()


    def start_client(self, port, ip_address):
        try:
            self.syncclipboard.start_client(ip_address, port)
        except Exception as e:
            self.showMsg.emit(f"An error occured while running the client: {e}", True)

        self.finished.emit()


    def print_msg(self, text):
        self.updateStatusLabel.emit(text)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main.ui", self)

        self.address_input = self.findChild(QLineEdit, "addressInput")

        validator = QIntValidator(1, 65535, self)
        self.port_input = self.findChild(QLineEdit, "portInput")
        self.port_input.setValidator(validator)

        self.action_mode = self.findChild(QComboBox, "comboBoxMode")
        self.start_button = self.findChild(QPushButton, "startButton")
        self.status_label = self.findChild(QLabel, "statusLabel")

        self.action_mode.currentTextChanged.connect(self.changeButtonText)
        self.start_button.clicked.connect(self.executeAction)

        self.worker = Worker()
        self.worker.finished.connect(self.actionFinished)
        self.worker.updateStatusLabel.connect(self.updateStatusLabel)
        self.worker.showMsg.connect(self.showMsg)

        self.show()


    def changeButtonText(self, currentText):
        if(currentText == "Server"):
            self.address_input.setText("")
            self.address_input.setEnabled(False)
            self.start_button.setText("Start as a server")
            self.updateStatusLabel("Ready to start as a server")
        else:
            self.address_input.setEnabled(True)
            self.start_button.setText("Start as a client")
            self.updateStatusLabel("Ready to start as a client")


    def executeAction(self):
        currentMode = self.action_mode.currentText()
        ip_address = self.address_input.text()
        port = self.port_input.text()

        if(currentMode == "Client"):
            if(not ip_address):
                self.showMsg("The IP address is empty! Please insert one")
                return False


        if(not port):
            self.showMsg("The port is empty! Please insert one")
            return False

        port = int(port)

        self.action_mode.setEnabled(False)
        self.start_button.setEnabled(False)

        if(currentMode == "Server"):
            thread = threading.Thread(target=self.worker.start_server, args=(port,))
        else:
            thread = threading.Thread(target=self.worker.start_client, args=(port, ip_address))

        thread.start()


    def actionFinished(self):
        currentText = self.action_mode.currentText()

        self.start_button.setEnabled(True)
        self.action_mode.setEnabled(True)

        self.changeButtonText(currentText)


    def showMsg(self, msgText, error=True):
        msg = QMessageBox()
        if(error):
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Error")
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Message")

        msg.setText(msgText)
        msg.exec_()


    def updateStatusLabel(self, text):
        self.status_label.setText(text)


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()