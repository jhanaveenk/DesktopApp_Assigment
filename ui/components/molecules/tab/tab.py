from PySide2.QtWidgets import QApplication, QLabel, QPushButton, QWidget,QSizePolicy, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,  QGridLayout, QFrame
from PySide2.QtCore import QSize, Qt, QRect, QPoint
import sys
from PySide2.QtGui import QPixmap, QImage
import os

class Tab(QWidget):

    def __init__(self, *args, **kwargs):
        super(Tab, self).__init__(*args, **kwargs)
        self.tab_btn = QPushButton()
        self.tab_layout = QHBoxLayout(self)
        self.image_label = QLabel()
        # self.setFixedSize(width, height)
        self.image_label.setFixedSize(24, 24)
        self.image_label.setPixmap(QPixmap(os.path.join("assets/close.png")).scaled(24, 24,  Qt.KeepAspectRatio))
        self.image_layout = QVBoxLayout(self)
        self.image_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        self.tab_layout.addWidget(self.tab_btn)
        self.tab_layout.addWidget(self.image_label)

        


    
