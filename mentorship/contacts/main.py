from PyQt5 import QtCore, QtGui, QtWidgets
from ADD import Ui_Add_MainWindow
from clear import Ui_ClearAll_MainWindow
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
import mysql.connector



class Ui_MainWindow(object):

    def open_add(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Add_MainWindow()
        self.ui.setupUi(self.window, MainWindow)
        self.window.show()
        #MainWindow.hide()


    def open_clear(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ClearAll_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    # Connect to data
    con = mysql.connector.connect(user='root', password='', host ='127.0.0.1', database='maktabkhoone')
    cur = con.cursor()

    # create table
    cur.execute(('''CREATE TABLE IF NOT EXISTS contacts (
                            id INT AUTO_INCREMENT PRIMARY KEY,
        	                name TEXT,
           	                email TEXT,
        	                phone TEXT
        	                )
                            ''')
                )

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 333)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.add_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_add())
        self.add_pushButton.setGeometry(QtCore.QRect(440, 20, 91, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_pushButton.setFont(font)
        self.add_pushButton.setObjectName("add_pushButton")
        self.del_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.delete_contact())
        self.del_pushButton.setGeometry(QtCore.QRect(440, 60, 91, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.del_pushButton.setFont(font)
        self.del_pushButton.setObjectName("del_pushButton")

        self.update_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.update())
        self.update_pushButton.setGeometry(QtCore.QRect(440, 100, 91, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.update_pushButton.setFont(font)
        self.update_pushButton.setObjectName("update_pushButton")

        self.edit_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.edit())
        self.edit_pushButton.setGeometry(QtCore.QRect(440, 140, 91, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_pushButton.setFont(font)
        self.edit_pushButton.setObjectName("edit_pushButton")

        self.clear_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_clear())
        self.clear_pushButton.setGeometry(QtCore.QRect(440, 260, 91, 33))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.clear_pushButton.setFont(font)
        self.clear_pushButton.setObjectName("clear_pushButton")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 411, 281))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        # Replace tabel with the name of the table you want to display
        self.cur.execute("SELECT * FROM contacts")
        data = self.cur.fetchall()

        # Set table dimensions
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(4)

        # Populate table with data
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

        # Optional: Set column headers
        column_names = [description[0] for description in self.cur.description]
        self.tableWidget.setHorizontalHeaderLabels(column_names)

        # Adjust column widths to fit contents
        self.tableWidget.resizeRowsToContents()



    def delete_contact(self):
        selected_items = self.tableWidget.selectedItems()
        item = selected_items[0].text()
        self.cur.execute("DELETE FROM contacts WHERE id = '%s' " % item)
        self.con.commit()

        rows_to_remove = set()
        for item in selected_items:
            rows_to_remove.add(item.row())

        # Remove rows in reverse order to avoid index issues
        for row in sorted(rows_to_remove, reverse=True):
            self.tableWidget.removeRow(row)

    def update_primary_keys(self):
        try:
            # Reset the auto-increment value to 1
            query = "ALTER TABLE contacts AUTO_INCREMENT = 1"
            self.cur.execute(query)
            self.con.commit()

            # Count the number of rows in the table
            self.cur.execute("SELECT COUNT(*) FROM contacts")
            row_count = self.cur.fetchone()[0]

            # Update primary key values
            for new_id in range(1, row_count + 1):
                query = "UPDATE contacts SET id = %s WHERE id = %s"
                self.cur.execute(query, (new_id, new_id + 1))
            self.con.commit()

            print("Primary keys reset and renumbered successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err.msg}")

    def edit(self):
        selected_items = self.tableWidget.selectedItems()
        item = selected_items[0].text()

        selected_indexes = self.tableWidget.selectedIndexes()
        selected_row = selected_indexes[0].row()
        first_block_data = self.tableWidget.item(selected_row, 0).text()

        # Assuming 'id' is the primary key column name
        contact_id = self.tableWidget.item(selected_row, 0).text()

        column_name = self.tableWidget.horizontalHeaderItem(selected_indexes[0].column()).text()

        # Update the contact information in the database
        query = f"UPDATE contacts SET {column_name} = %s WHERE id = %s"
        values = (item, contact_id)

        self.cur.execute(query, values)
        self.con.commit()

    def update(self):

        self.update_primary_keys()
        # Clear existing data in the table
        self.tableWidget.clearContents()

        # Fetch data from the database
        self.cur.execute("SELECT * FROM contacts")

        data = self.cur.fetchall()

        # Set table dimensions
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(4)

        # Populate table with data
        for row_num, row_data in enumerate(data):
            for col_num, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

        # Optional: Set column headers
        column_names = [description[0] for description in self.cur.description]
        self.tableWidget.setHorizontalHeaderLabels(column_names)

        # Adjust column widths to fit contents
        self.tableWidget.resizeRowsToContents()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Contacts"))
        self.add_pushButton.setText(_translate("MainWindow", "Add.."))
        self.del_pushButton.setText(_translate("MainWindow", "Delete"))
        self.clear_pushButton.setText(_translate("MainWindow", "Clear All"))
        self.update_pushButton.setText(_translate("MainWindow", "Update"))
        self.edit_pushButton.setText(_translate("MainWindow", "Edit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
