from PySide2.QtWidgets import QApplication, QSizePolicy, QLabel, QComboBox, QMenuBar, QMenu, QPushButton, QFrame,  QWidget, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout
from PySide2.QtCore import QSize, Qt, QByteArray,Signal, QThread, QTimer, QTime, QEventLoop
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from random import *
from PySide2.QtGui import QPixmap, QMovie
import os
import time


# class LoadThread(QThread):
    
#     def __init__(self, *args, **kwargs):
#         QThread.__init__(self, *args, **kwargs)

#         self.timer = QTimer()


#     pass


class Loader(QWidget):
    __instance = None
    def __init__(self):

        if Loader.__instance is not None:
            raise Exception("This is singleton class")
        else:
            Loader.__instance = self    
             
        super().__init__() 
        self.setGeometry(400, 200, 50, 50)
        self.setWindowTitle("Loader")
        self.movie_screen = QLabel()
         
    
        self.movie_screen.setSizePolicy(QSizePolicy.Expanding, 
            QSizePolicy.Expanding)        

        self.movie_screen.setAlignment(Qt.AlignCenter) 



        # positin the widgets
        main_layout = QVBoxLayout() 
        main_layout.addWidget(self.movie_screen)
        self.setLayout(main_layout) 


        ag_file =  os.path.join("assets/loader.gif")
        self.movie = QMovie(ag_file, QByteArray(), self) 
        self.movie.setCacheMode(QMovie.CacheAll) 
        self.movie.setSpeed(100) 
        self.movie_screen.setMovie(self.movie) 
        self.movie.start()


    def start(self):
        """sart animnation"""
        self.movie.start()
        
    def stop(self):
        """stop the animation"""
        self.movie.stop()