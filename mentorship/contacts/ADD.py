import mysql.connector, pymysql
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
import re


class Ui_Add_MainWindow(object):
    # Connect to data
    con = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='maktabkhoone')
    cur = con.cursor()

    def setupUi(self, Add_MainWindow, MainWindow):
        Add_MainWindow.setObjectName("Add_MainWindow")
        Add_MainWindow.resize(344, 231)
        font = QtGui.QFont()
        font.setPointSize(10)
        Add_MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(Add_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cancel_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.close(Add_MainWindow))
        self.cancel_pushButton.setGeometry(QtCore.QRect(80, 150, 81, 33))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.cancel_pushButton.setFont(font)
        self.cancel_pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.OK_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.AddData(Add_MainWindow))
        self.OK_pushButton.setGeometry(QtCore.QRect(200, 150, 81, 33))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.OK_pushButton.setFont(font)
        self.OK_pushButton.setCheckable(False)
        self.OK_pushButton.setObjectName("OK_pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 61, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 60, 58, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 100, 65, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.name_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.name_lineEdit.setGeometry(QtCore.QRect(130, 19, 151, 31))
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.email_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.email_lineEdit.setGeometry(QtCore.QRect(130, 60, 151, 31))
        self.email_lineEdit.setObjectName("email_lineEdit")
        self.phone_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.phone_lineEdit.setGeometry(QtCore.QRect(130, 100, 151, 31))
        self.phone_lineEdit.setText("")
        self.phone_lineEdit.setObjectName("phone_lineEdit")
        Add_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Add_MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 344, 21))
        self.menubar.setObjectName("menubar")
        Add_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Add_MainWindow)
        self.statusbar.setObjectName("statusbar")
        Add_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(Add_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(Add_MainWindow)

    def close(self, sec_w):
        sec_w.hide()

    def checkmail(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        email = self.email_lineEdit.text()
        return re.match(pattern, email)

    def AddData(self, sec_w):
        # info that user give
        esm = self.name_lineEdit.text().title()
        email = self.email_lineEdit.text()
        phone = self.phone_lineEdit.text()

        if self.checkmail(email) is not None:
            # Add to table
            self.cur.execute("INSERT INTO contacts (name, email, phone) VALUES (%s, %s, %s)", (esm, email, phone))
            self.con.commit()
            sec_w.hide()
        else:
            self.email_lineEdit.setText("Wrong Email format!")

    def retranslateUi(self, Add_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        Add_MainWindow.setWindowTitle(_translate("Add_MainWindow", "Add Contact"))
        self.cancel_pushButton.setText(_translate("Add_MainWindow", " Cancel"))
        self.OK_pushButton.setText(_translate("Add_MainWindow", "OK"))
        self.label.setText(_translate("Add_MainWindow", "Name:"))
        self.label_2.setText(_translate("Add_MainWindow", "Email:"))
        self.label_3.setText(_translate("Add_MainWindow", "Phone:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Add_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Add_MainWindow()
    ui.setupUi(Add_MainWindow)
    Add_MainWindow.show()
    sys.exit(app.exec_())



