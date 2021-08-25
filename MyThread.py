from PyQt5.QtCore import QThread,QDir,QObject

import stagger

from mutagen.id3 import ID3
import io
import os
from MyCustomWidget import MyWidget

from PIL import Image



class Work(QObject):
    """ I'll do the work and live in the worker thread!"""

    def __init__(self,list,listofsongs,directory = ''):
        self.list = list
        self.listofsongs = listofsongs

        self.directory = directory
        super(__class__, self).__init__()

    def BinToPixmap(self,artwork,name):
        im = Image.open(artwork)


        im.save("images/"+name+"."+im.format)
        path = "images/"+name+"."+im.format

        return path
















    def doWork(self):
        if self.directory != "":
            extension = '.mp3'
            for root, directories, filenames in os.walk(self.directory):
                for filename in filenames:
                    if filename.endswith(extension):
                        myWidget = MyWidget()

                        try:
                            audio = ID3(root + '/' + filename)
                            myWidget.setName(audio['TIT2'].text[0])

                            self.listofsongs[audio['TIT2'].text[0]] = str(root + '/' + filename)


                            self.list.addItem(myWidget)



                        except:
                            myWidget.setName(filename)
                            self.listofsongs[filename] = str(root + '/' + filename)

                            self.list.addItem(myWidget)

                        try:
                            mp3 = stagger.read_tag(root + '/' + filename)
                            data = io.BytesIO(mp3[stagger.id3.APIC][0].data)
                            path = self.BinToPixmap(data, filename)
                            myWidget.setImage(path)
                            self.list.addItem(myWidget)
                        except:

                            myWidget.setImage("icons/magic.jpg")

                            self.list.addItem(myWidget)


            self.list.setSortingEnabled(True)
            self.list.sortItems()



class MyThread(QThread):
    """ I'm just going to setup the event loop and do
        nothing else..."""

    def __init__(self,list,listofsongs,directory = ''):
        self.list = list
        self.listofsongs = listofsongs
        self.directory = directory
        super(QThread, self).__init__()

    def run(self):
        self.work = Work(self.list,self.listofsongs,self.directory)
        self.work.doWork()
65


