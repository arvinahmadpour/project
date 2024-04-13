from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import sys
import requests
import mysql.connector
from datetime import datetime


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load UI
        uic.loadUi("Weather.ui", self)

        # Define our widgets
        self.get = self.findChild(QPushButton, "pushButton")
        self.location_input = self.findChild(QLineEdit, "lineEdit")
        self.city_info = self.findChild(QLabel, "description")
        self.temp = self.findChild(QLabel, "temp_label")
        self.high = self.findChild(QLabel, "high_label")
        self.low = self.findChild(QLabel, "low_label")
        self.title = self.findChild(QLabel, "title")
        self.icon = self.findChild(QLabel, "tempicon_label")

        self.icon.setVisible(False)

        self.get.clicked.connect(self.get_weather)

        self.get_info()

        self.show()

    # Connect to data
    con = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='learn')
    cur = con.cursor()
    # create table
    cur.execute(('''CREATE TABLE IF NOT EXISTS Weathers (
            	                name TEXT,
               	                temp TEXT,
            	                feels_like TEXT,
            	                humidity TEXT,
            	                description TEXT
            	                )
                                '''))

    def get_info(self):
        city = self.location_input.text()
        key = "c40a990cc5070e01e539075ecec2b10a"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}"
        state = requests.get(url)
        info = state.json()
        return info

    def reset_info(self):
        self.city_info.setText('')
        self.temp.setText('')
        self.high.setText('')
        self.low.setText('')
        self.icon.setVisible(False)


    def get_weather(self):
        data = self.get_info()
        if data['cod'] != '404':
            temp = data['main']['temp'] - 273.15
            high =  data['main']['temp_max'] - 273.15
            low = data['main']['temp_min'] - 273.15
            feels_like = data['main']['feels_like'] - 273.15
            description = data['weather'][0]['description']
            humidity = data ['main']['humidity']
            Info_time = int(data["dt"])
            Info_time = datetime.utcfromtimestamp(Info_time).strftime("%Y-%m-%d %H:%M:%S")

            description =f"""
            {description}
            """

            header = f"""
            {self.location_input.text().title()}
            {Info_time}
            """
            self.icon.setVisible(True)

            self.city_info.setText(description)
            self.temp.setText(f'{temp:.1f}')
            self.high.setText(f'H: {high:.1f}')
            self.low.setText(f'H: {low:.1f}')
            self.title.setText(header)

        else:
            self.title.setText("City not found !!!")
            self.reset_info()



# Initialized the app
app = QApplication(sys.argv)
Uiwindow = UI()
app.exec_()