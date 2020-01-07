import sys


from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QMessageBox, QMainWindow, QVBoxLayout, QPushButton, QWidget, QApplication, QHBoxLayout,
                             QPlainTextEdit, QShortcut)
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

import googleFireBaseCommunication

class Stick(QMainWindow):  # klasa rozszerzona o moduł QMainWindow



    def __init__(self):  # konstruktor, #self trzeba explicit poddawać by konstruktor wiedział, że odwołujemy się do klasy Stick
        super().__init__()  # dostęp do wewnetrznych funkcji QMainWindow

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.resize(264, 279)

        self.setWindowTitle("mojStick")
        self.textField = QPlainTextEdit()

        checkFireBaseButton = QPushButton("Check Firebase")
        checkFireBaseButton.clicked.connect(self.lookUpGDrive)

        closeButton = QPushButton("X")
        closeButton.clicked.connect(self.closeEvent)

        saveButton = QPushButton("Save")
        saveButton.clicked.connect(self.updateToGoogle)


        self.mainLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.buttonLayout)

        self.buttonLayout.addWidget(checkFireBaseButton)
        self.buttonLayout.addWidget(closeButton)

        self.mainLayout.addWidget(self.textField)
        self.mainLayout.addWidget(saveButton)

        widget = QWidget()

        sizegrip = QtWidgets.QSizeGrip(widget)  # QSizeGrip - klasa umożliwiająca resizing
        self.mainLayout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        widget.setLayout(self.mainLayout)

        self.setCentralWidget(widget)
        self.loadStyleSheet()

        shortcut = QShortcut(QKeySequence("Ctrl+S"), self.textField)
        shortcut.activated.connect(self.saveCtrlS)


    def updateStickText(self,textToUpdate):

        self.textField.setPlainText(textToUpdate)


    def lookUpGDrive(self):

        textFromServer = googleFireBaseCommunication.getStickValue()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Note imported from Firebase:")
        msg.setInformativeText(textFromServer)

        sendToGDriveButton = msg.addButton(
            'Send local to Firebase', QtWidgets.QMessageBox.AcceptRole)

        downloadFromGDrive = msg.addButton(
            'Download stick from Firebase and overwrite local', QtWidgets.QMessageBox.AcceptRole)

        msg.addButton("X", QtWidgets.QMessageBox.RejectRole)

        msg.exec_()  # displays messagebox in new window
        msg.deleteLater()

        if msg.clickedButton() is sendToGDriveButton:
            self.updateToGoogle()
        elif msg.clickedButton() is downloadFromGDrive:
            self.downloadFromGoogle()
            self.saveLocally()
        else:
            msg.close()

        stick.mainLayout.addWidget(msg)



    def downloadFromGoogle(self):

        self.textField.setPlainText(googleFireBaseCommunication.getStickValue())
        self.saveLocally()

    def updateToGoogle(self):

        if self.textField.toPlainText() == googleFireBaseCommunication.getStickValue():

            popupWindowError = QMessageBox.about(self, 'Error', "Already up to date")
            stick.mainLayout.addWidget(popupWindowError)

        else:

            googleFireBaseCommunication.updateStick(self.textField.toPlainText())
            popupWindowSuccess = QMessageBox.about(self, 'Success', "Updated succesfully")
            stick.mainLayout.addWidget(popupWindowSuccess)
            self.saveLocally()

    def loadStyleSheet(self):

        css = """

        QPlainTextEdit{

            background: #fad50c;
            font-size: 17px;

        }
      
  

        """
        self.setStyleSheet(css)

    def saveLocally(self):
        mytext = self.textField.toPlainText()
        with open('notatka.txt', 'w') as notatka:
            notatka.write(mytext)

    def loadStickFromFile(self):

        with open("notatka.txt", "r") as notatka:
            textFromFile = notatka.read()

        return textFromFile

    def closeEvent(self, event):


        sys.exit(app.exec_())

    def saveCtrlS(self):
        self.saveLocally()


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


if __name__ == '__main__':
    app = QApplication(sys.argv)


    stick = Stick()  # konstrukcja obiektu
    stick.show()
    stick.downloadFromGoogle() #getting the latest value from firebase


    sys.exit(app.exec_())
