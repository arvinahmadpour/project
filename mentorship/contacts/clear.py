from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector

class Ui_ClearAll_MainWindow(object):
    # Connect to data
    con = mysql.connector.connect(user='root', password='', host ='127.0.0.1', database='maktabkhoone')
    cur = con.cursor()

    def setupUi(self, ClearAll_MainWindow):
        ClearAll_MainWindow.setObjectName("ClearAll_MainWindow")
        ClearAll_MainWindow.resize(451, 199)
        self.centralwidget = QtWidgets.QWidget(ClearAll_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 40, 389, 25))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.close(ClearAll_MainWindow))
        self.pushButton.setGeometry(QtCore.QRect(90, 110, 111, 33))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda : self.clear_list(ClearAll_MainWindow))
        self.pushButton_2.setGeometry(QtCore.QRect(250, 110, 111, 33))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setObjectName("pushButton_2")
        ClearAll_MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ClearAll_MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 451, 21))
        self.menubar.setObjectName("menubar")
        ClearAll_MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ClearAll_MainWindow)
        self.statusbar.setObjectName("statusbar")
        ClearAll_MainWindow.setStatusBar(self.statusbar)
        self.actiondelete = QtWidgets.QAction(ClearAll_MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../Downloads/Programs/pyqt/icons/ui-toolbar--exclamation.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actiondelete.setIcon(icon)
        self.actiondelete.setObjectName("actiondelete")

        self.retranslateUi(ClearAll_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(ClearAll_MainWindow)

    def close(self, third_w):
        third_w.hide()

    def clear_list(self, third_W):
        self.cur.execute("DELETE FROM contacts")
        self.con.commit()
        third_W.hide()


    def retranslateUi(self, ClearAll_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        ClearAll_MainWindow.setWindowTitle(_translate("ClearAll_MainWindow", "Warning!"))
        self.label.setText(_translate("ClearAll_MainWindow", "Do you want to remove all your contacts?"))
        self.pushButton.setText(_translate("ClearAll_MainWindow", " Cancel"))
        self.pushButton_2.setText(_translate("ClearAll_MainWindow", "OK"))
        self.actiondelete.setText(_translate("ClearAll_MainWindow", "delete"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ClearAll_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_ClearAll_MainWindow()
    ui.setupUi(ClearAll_MainWindow)
    ClearAll_MainWindow.show()
    sys.exit(app.exec_())
