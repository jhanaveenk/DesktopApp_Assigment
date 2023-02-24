from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QWidget,QSizePolicy, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,  QGridLayout, QFrame
from PySide2.QtCore import QSize, Qt, QRect, QPoint
import sys
from ui.components.molecules.tab.tab import Tab
from ui.components.molecules.tab.tabs import Tabs
from PySide2.QtGui import QPixmap, QImage
import os

class ImageFrame(QFrame):

    def __init__(self, path, width=64, height=64, xpos=0, ypos=0, *args, type, **kwargs):

        super(ImageFrame, self).__init__()
        self.image_label = QLabel()
        # self.setFixedSize(width, height)
        self.image_label.setFixedSize(width, height)
        self.setStyleSheet(f"""
        background : { "green" if type == "good" else "red" } ;
        border-width : 10px;
        border-color : blue;
        """)
        self.image_label.setPixmap(QPixmap(path).scaled(width, height,  Qt.KeepAspectRatio))
        self.image_layout = QVBoxLayout(self)
        self.image_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

    

        
        
