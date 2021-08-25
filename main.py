import sys

from PyQt5.QtWidgets import (QWidget,QMainWindow , QPushButton, QFileDialog,QVBoxLayout,QListWidget,
     QApplication,QSlider,QStyle,QAction)
from PyQt5.QtGui import QIcon,QPalette,QBrush,QPixmap,QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import Qt,QSize,QDir,QUrl,QFile,QStringListModel

from GUI import Ui_MainWindow
from MyThread import MyThread


class Player(QMainWindow):
    listofsongs = {}


    def __init__(self):
      super().__init__()
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      self.initUI()
      self.show()


    def initUI(self):
        animeTheme = QAction(QIcon('new.png'), 'AnimeTheme',self)
        animeTheme.triggered.connect(self.chooseAnimeTheme)

        filemenu = self.ui.menubar.addMenu('SetTheme')
        filemenu.addAction(animeTheme)


        self.ui.MusicImage.setAlignment(Qt.AlignCenter)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.ui.search_song.textChanged.connect(self.search)

        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)

        self.ui.sld.setRange(0, 0)
        self.ui.sld.sliderMoved.connect(self.setPosition)




        self.ui.pause_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.ui.pause_btn.clicked.connect(self.play)










        self.ui.list.setFont(QFont("TimesNewRoman",11))
        self.ui.list.clicked.connect(self.item_clicked)




        self.ui.list.setIconSize(QSize(64,64))













        self.setStyleSheet("QMainWindow{background-image: url(sky.jpg);background-repeat: no-repeat;}")




        self.mythread = MyThread(self.ui.list, self.listofsongs, directory=QDir.homePath())
        self.mythread.start()
    def chooseAnimeTheme(self):
        with open("theme/animeTheme.txt") as file:
            data = file.read().replace('\n'," ")
            print(data)
            self.setTheme(data)

    def chooseStandartTheme(self):
        self.setTheme("Player/theme/animeTheme.ss")

    def setTheme(self,stylesheet):
       # self.setStyleSheet(stylesheet)
        self.setStyleSheet(
            "QListView{background-color:transparent;border-style:transparent;}"

        )


    def search(self):
        text = self.ui.search_song.text()
        print(self.ui.list.findItems(text,Qt.MatchStartsWith))



    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "change directory",
                QDir.homePath())

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.ui.pause_btn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.ui.pause_btn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.ui.sld.setValue(position)

    def durationChanged(self, duration):
        self.ui.sld.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def addItems(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.mythread = MyThread(self.list,self.listofsongs,directory=directory)
        self.mythread.start()



    def item_clicked(self):
        item = self.ui.list.currentItem()
        self.ui.MusicImage.setPixmap(QPixmap(item.getImagePath()))
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.listofsongs[(str(item.text()))])))
        #print(self.mediaPlayer.currentMedia().canonicalUrl().toString())

        self.mediaPlayer.play()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Player()
    sys.exit(app.exec_())