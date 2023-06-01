import sys

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, \
    QPushButton, QComboBox, QLineEdit, \
        QMessageBox, QFileDialog
from PyQt5 import uic
from PyQt5.Qt import  QIntValidator

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
        self.showMsg("Você está clicando realmente no botão!", False)


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