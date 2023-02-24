from PySide2.QtWidgets import   QApplication, QComboBox, QMenuBar, QMenu, QPushButton, QFrame,  QWidget, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout
from PySide2.QtCore import QSize, Qt
import sys
from PySide2.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from model.setup import MongoDb
import os 
from random import *
import time
from ui.components.molecules.loader.loader import Loader


class Paginator(QWidget):

    def __init__(self,parent,  items_per_page = 20, *args, **kwargs):  
        self.parent = parent
        data = self.parent.filtered_items
        super(Paginator, self).__init__(*args, **kwargs)
        self.items_per_page = items_per_page
        self.page_count = len(data)//self.items_per_page + len(data)%items_per_page
        self.page_layout = QHBoxLayout(self)
        self.handle_paginate = self.parent._pagination
        self.add_page_buttons()

    def clear_panel(self):
        while ((child := self.page_layout.takeAt(0)) != None):
            child.widget().deleteLater()

    def render(self):
        self.clear_panel()
        self.update_data()
        self.add_page_buttons()

    def update_data(self):
        print("parent data length", len(self.parent.filtered_items))

        data = self.parent.filtered_items
        self.page_count = len(data)//self.items_per_page + ( 1 if len(data)%self.items_per_page  else 0 )
        print(self.page_count)


    def add_page_buttons(self):

        self.setMaximumWidth( self.page_count*40 + 10)
        self.page_left_btn = QPushButton()
        self.page_left_btn.setIcon( QIcon(os.path.join("assets/left-arrow.png") ))
        self.page_left_btn.clicked.connect(lambda item : self.handle_arrow_btn(-1))
        self.page_right_btn = QPushButton()
        self.page_right_btn.setIcon( QIcon(os.path.join("assets/right-arrow.png")))
        self.page_right_btn.clicked.connect(lambda  item: self.handle_arrow_btn(1))


        self.page_layout.addWidget(self.page_left_btn)
        for  index in list(range(self.page_count)):
            btn = QPushButton(str(index))
            text: int = int(btn.text())

            try:
                if   index == self.parent.curr_page_pointer:
                    btn.setStyleSheet("background : grey;")
                else:
                    btn.setStyleSheet("background : white;")
            except Exception as e:
                print(e)


            lambda_func = (
                    lambda int = int, text = text: self.handle_page_btns(
                        text
                    )
                )
            self.page_layout.addWidget(btn, alignment = Qt.AlignRight)
            btn.clicked.connect(lambda_func)             

        self.page_layout.addWidget(self.page_right_btn)

    def handle_page_btns(self, index, **kwargs):
        print("index : ", index, kwargs)
        self.handle_paginate(index)
        self.render()
    def handle_arrow_btn(self, value):
        print("handle_arrow")
        self.handle_paginate((self.parent.curr_page_pointer + value)% self.page_count )
        self.render()
