from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
import sys, os, time
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, QTimer, Qt
from pygame import mixer

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load UI
        uic.loadUi("MusicPlayer.ui", self)

        # Define our widgets
        self.MusicList = self.findChild(QListWidget, "listWidget")
        self.MusicTime = self.findChild(QSlider, "horizontalSlider")
        self.Play = self.findChild(QPushButton, "Play_pushButton")
        self.Pause = self.findChild(QPushButton, "Pause_pushButton")
        self.Volume = self.findChild(QDial, "dial")
        self.Next = self.findChild(QPushButton, "Next_pushButton")
        self.Previous = self.findChild(QPushButton, "Previous_pushButton")
        self.Stop = self.findChild(QPushButton, "Stop_pushButton")
        self.songname = self.findChild(QLabel, "songname_label")
        self.volumestate = self.findChild(QLabel, "V_label")
        self.start = self.findChild(QLabel, "V_label")
        self.V_status = self.findChild(QLabel, "V_label")
        self.end = self.findChild(QLabel, "End_label")
        self.start = self.findChild(QLabel, "Start_label")
        self.rem = self.findChild(QPushButton, "Remove_pushButton")
        self.remA = self.findChild(QPushButton, "removeall_pushButton")
        self.mute = self.findChild(QPushButton, "Mute_pushButton")
        self._radio_button = self.findChild(QRadioButton, "radioButton")

        # action button
        self.Play.clicked.connect(self.play)

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        self.Pause.clicked.connect(self.pause)
        self.Stop.clicked.connect(self.stop)
        self.Next.clicked.connect(self.next)
        self.Previous.clicked.connect(self.previous)
        self.rem.clicked.connect(self.remove)
        self.remA.clicked.connect(self.remove_all)
        self.actionOpen.triggered.connect(self.addsong)
        self.mute.clicked.connect(self.mutesong)

        self.MusicList.doubleClicked.connect(self.play)

        self._radio_button.toggled.connect(self.toggle_repeat)

        self.repeat = False

        self.player.mediaStatusChanged.connect(self.check_end_of_media)

        # Use dial
        self.dial.valueChanged.connect(lambda: self.dialer())
        self.dial.setStyleSheet('background-color: blue')
        self.dial.setNotchesVisible(True)
        self.dial.setRange(0, 100)
        self.dial.setValue(50)
        self.V_status.setText("50")
        self.current_volume = 50

        self.player.setVolume(self.current_volume)

        # toolbar
        action_open = QAction("Open", self)
        action_open.triggered.connect(self.addsong)

        self.Mlist = []

        global stopped
        stopped = False
        self.paused_position = 0

        # Slider Timer
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.move_slider)

        # show
        self.show()

    def addsong(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Open Files", "", "Audio Files (*);;*.mp3;;*.mpeg;;*.ogg;;*.m4a;;*.MP3;;*.wma;;*.acc;;*.amr")
        if files:
            for song in files:
                self.Mlist.append(song)
                song = song.split('/')[-1]
                self.MusicList.addItem(song)

    def pause(self):
        try:
            global stopped
            stopped = True
            self.paused_position = self.player.position()  # Store the current position
            self.player.pause()
        except Exception as e:
            print(f"Pause song error: {e}")

    def play(self):
        try:
            global stopped
            stopped = False

            current_selection = self.listWidget.currentRow()
            current_song = self.Mlist[current_selection]

            self.songname.setText(os.path.basename(current_song))

            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)

            if self.paused_position:
                self.player.setPosition(self.paused_position)
                self.player.play()  # Resume playing from the stored position
                self.move_slider()
            else:
                self.player.play()
                self.move_slider()

            self.paused_position = 0  # Reset the paused position

        except Exception as e:
            print(f"Play song error: {e}")

    def mutesong(self):
        self.player.setMuted(not self.player.isMuted())

    def next(self):
        try:
            current_selection = self.MusicList.currentRow()

            if current_selection + 1 == len(self.Mlist):
                next_index = 0
            else:
                next_index = current_selection + 1
            current_song = self.Mlist[next_index]
            self.MusicList.setCurrentRow(next_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.songname.setText(os.path.basename(current_song))
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Next song error: {e}")

    def previous(self):
        try:
            current_selection = self.MusicList.currentRow()

            if current_selection == 0:
                previous_index = len(self.Mlist) - 1
            else:
                previous_index = current_selection - 1

            current_song = self.Mlist[previous_index]
            self.MusicList.setCurrentRow(previous_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.songname.setText(os.path.basename(current_song))
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Previous song error: {e}")

    def stop(self):
        self.player.stop()
        self.MusicTime.setValue(0)
        self.start.setText(f"00:00:00")
        self.end.setText(f"00:00:00")

    def move_slider(self):
        if stopped:
            return
        else:
            # Update the slider
            if self.player.state() == QMediaPlayer.PlayingState:
                self.MusicTime.setMinimum(0)
                self.MusicTime.setMaximum(self.player.duration())
                slider_position = self.player.position()
                self.MusicTime.setValue(slider_position)

                current_time = time.strftime('%H:%M:%S', time.gmtime(self.player.position() / 1000))
                song_duration = time.strftime('%H:%M:%S', time.gmtime(self.player.duration() / 1000))
                self.start.setText(f"{current_time}")
                self.end.setText(f"{song_duration}")

    def remove(self):
        current_selection = self.listWidget.currentRow()
        self.Mlist.pop(current_selection)
        self.MusicList.takeItem(current_selection)

    def remove_all(self):
        self.stop()
        self.MusicList.clear()
        self.Mlist.clear()
        self.songname.setText("")

    def dialer(self):
        try:
            self.current_volume = self.Volume.value()
            self.player.setVolume(self.current_volume)
            self.V_status.setText(f"{self.current_volume}")
        except Exception as e:
            print(f"Changing volume error: {e}")

    def toggle_repeat(self, checked):
        self.repeat = checked

    def check_end_of_media(self, status):
        if status == QMediaPlayer.EndOfMedia and self.repeat:
            self.player.setPosition(0)
            self.play()

# Initialized the app
app = QApplication(sys.argv)
Uiwindow = UI()
app.exec_()