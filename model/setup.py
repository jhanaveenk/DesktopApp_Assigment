import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
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

from ui.components.molecules.loader.loader import Loader
load_dotenv()
DB_LINK = str(os.getenv("DB"))  

class MongoDb:
    def __init__(self, host : str = "localhost", port : int = 27017,  db : str= "SWITCHON", collection : str = "naveenswitchon") -> None:
        self.__cluster = MongoClient()
        self.__db = self.__cluster[db]
        self.__collection = self.__db[collection]

    def __enter__(self):
        return self

    def connection(self):
        return self.__collection

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.__cluster.close()
    
    