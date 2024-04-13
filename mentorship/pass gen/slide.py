from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QSlider, QLabel, QLineEdit, QCheckBox
from PyQt5 import uic
import sys
import random, string

class UI(QMainWindow):
    set_pass =''
    def __init__(self):
        super(UI, self).__init__()

        # Load UI
        uic.loadUi("password.ui", self)

        # Define our widgets
        self.slider = self.findChild(QSlider, "horizontalSlider")
        self.label = self.findChild(QLabel, "label")
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        self.g_button = self.findChild(QPushButton, "pushButton")
        self.c_button = self.findChild(QPushButton, "copy_pushButton")
        self.upper = self.findChild(QCheckBox, "Uppercase_checkBox")
        self.lower = self.findChild(QCheckBox, "Lowercase_checkBox")
        self.symbol = self.findChild(QCheckBox, "Symbols_checkBox")
        self.number = self.findChild(QCheckBox, "Numbers_checkBox")

        # set slider properties
        self.slider.setMinimum(3)
        self.slider.setMaximum(50)
        self.slider.setValue(5)

        # Move slider
        self.slider.valueChanged.connect(self.slide_it)

        # set default check box to checked
        self.number.setChecked(True)

        # Line edit start text
        self.lineEdit.setText(" Let's generate password for you!!")

        # Update checkboxes
        self.lower.toggled.connect(lambda: self.password())
        self.upper.toggled.connect(lambda: self.password())
        self.symbol.toggled.connect(lambda: self.password())
        self.number.toggled.connect(lambda: self.password())

        # Click GENERATE
        self.g_button.clicked.connect(self.generator)

        # Click copy
        self.c_button.clicked.connect(self.copy_pass)

        # show
        self.show()

    def slide_it(self, value):
        self.label.setText(f'lenght: {str(value)}')
        length = value

    def password(self):
        # create char list for random selecting
        Char = ''

        # Char types selected
        options = 0

        # check which options are selected
        if self.lower.isChecked() == True:
            Char += string.ascii_lowercase
            options += 1
        if self.upper.isChecked() == True:
            Char += string.ascii_uppercase
            options += 1
        if self.symbol.isChecked() == True:
            Char += '!@#$%^&*'
            options += 1
        if self.number.isChecked() == True:
            Char += '0123456789'
            options += 1

        # generate random pass
        if options != 0:
            # user select at least one option
            self.set_pass = ''
            for i in range(self.slider.value()):
                # choosing random char
                self.set_pass += random.choice(Char)
        else:
            # user did not select any option
            self.lineEdit.setText('select at least one item please!')
            self.set_pass = ''

    def generator(self):
        self.password()
        # check is there any pass in box
        if self.set_pass == '':
            self.lineEdit.setText('select at least one item please!')
        else:
            self.lineEdit.setText(self.set_pass)

    def copy_pass(self):
        # check is there any pass to copy it
        if self.lineEdit.text() == 'select at least one item please!':
            self.lineEdit.setText("There is nothing here!!! ")
        else:
            # Get text from QLineEdit
            text_to_copy = self.lineEdit.text()
            # Copy text to clipboard
            QApplication.clipboard().setText(text_to_copy)

# Initialized the app
app = QApplication(sys.argv)
Uiwindow = UI()
app.exec_()