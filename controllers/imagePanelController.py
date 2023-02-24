from PySide2.QtWidgets import QFrame, QApplication, QSizePolicy, QScrollArea, QLabel, QPushButton, QWidget, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout,  QGridLayout
from PySide2.QtCore import QSize, Qt, QRect, QPoint
import sys
from ui.components.molecules.tab.tab import Tab
from ui.components.molecules.tab.tabs import Tabs
from PySide2.QtGui import QPixmap
from ui.components.atoms.ImageFrame import ImageFrame
from model.setup import MongoDb
from PIL import Image 
import PIL
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor, wait
import shutil
from threading import Thread
import glob
from datetime import datetime
from controllers.paginatorPanelController import Paginator

ASSETS_FILE_PATH  = os.path.join("./assets/")

class ImageGalleryPanel(QWidget):

    def __init__(self,parent, *args, **kwargs):
        
        super(ImageGalleryPanel, self).__init__(*args, **kwargs)
        self.parent = parent
        self._layout = QVBoxLayout()
        self.sku_items_list = self.parent._sku_list
        self.filtered_items = self.sku_items_list
        self.current_sku = self.parent._current_sku
        self.paginator = Paginator(self, 20)
        self.curr_page_pointer = 0
        self.add_filters()
        self.add_image_grid()
        self._layout.addWidget(self.paginator)
        self.__display_filtered_data()
        self.setLayout(self._layout)



    def _pagination(self, index):
        self.curr_page_pointer = index
        self.clear_panel()
        self.__display_filtered_data()


    def add_image_grid(self):
        self.scroll_area = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll_area.setStyleSheet("background : black;")
        self.scroll_frame = QFrame()
        self.scroll_area.setWidget(self.scroll_frame)
        # self.scroll_frame.setFixedSize(400, 500)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_frame.setLayout( QGridLayout())

        self.scroll_frame.setFixedSize(1200, 800)
        self._layout.addWidget(self.scroll_area)


    def add_filters(self):
        self.filter_container = QWidget()
        self.filter_layout = QHBoxLayout(self.filter_container)
        self.filter_layout.setDirection(QHBoxLayout.RightToLeft)
        self.filter_layout.setSpacing(0)
        self.filter_container.setMaximumWidth(350)
        self.filter_container.setMinimumWidth(200)
        self.bad_filter = QPushButton('Bad')
        self.bad_filter.setMaximumSize(QSize(50, 20))
        self.bad_filter.clicked.connect(lambda : self.filter("bad"))

        self.good_filter = QPushButton('Good')
        self.good_filter.clicked.connect(lambda : self.filter("good"))
        self.good_filter.setMaximumSize(QSize(50, 20))

        self.all_filter = QPushButton('All')
        self.all_filter.setMaximumSize(QSize(50, 20))
        self.all_filter.clicked.connect(lambda : self.filter("all"))
        
        self.filter_layout.addWidget(self.all_filter)
        self.filter_layout.addWidget(self.bad_filter)
        self.filter_layout.addWidget(self.good_filter)

        self._layout.addWidget(self.filter_container, alignment = Qt.AlignRight)

        

    def __display_filtered_data(self):
        col_size = 4
        total_no_of_img = self.paginator.items_per_page
        start_index = self.curr_page_pointer*total_no_of_img
        end_index = start_index + total_no_of_img
        print("render images - ", total_no_of_img )
        self.filtered_items = list(filter( lambda item : item.get("sku_id") == self.current_sku, self.filtered_items))

        paginated_data = self.filtered_items[start_index : end_index + 1]
        
        COL_SIZE = 6
        ROW_SIZE = len(paginated_data)//COL_SIZE + ( 1 if len(paginated_data)%COL_SIZE else 0  )
        
        for row in range(0, ROW_SIZE):
            for col in range(0, COL_SIZE) :
                img_data = paginated_data[ row + col ]
                image = ImageFrame(img_data.get("path"), 100, 100, type = img_data.get("status"))
                self.scroll_frame.layout().addWidget(image, row, col )
        
        self.paginator.render()

    def clear_panel(self):
        while ((child := self.scroll_frame.layout().takeAt(0)) != None):
            child.widget().deleteLater()

    def paginate_data(self):
        start = self.curr_page_pointer*self.paginator.items_per_page
        end = self.paginator.items_per_page + start
        # self.filtered_items = self.sku_items_list[start : end + 1 ]
        print("start, end", start, end)

    def filter(self, target,  *args, **kwargs):
        self.curr_page_pointer = 0
        if target == "all":
            self.filtered_items = self.sku_items_list
        else:
            self.filtered_items = list(filter( lambda x : x.get("status") == target  , self.sku_items_list))
        
        self.filtered_items = list(filter( lambda item : item.get("sku_id") == self.current_sku, self.filtered_items))

        self._pagination(self.curr_page_pointer)
        self.paginator.render()

    def __get_data(self):
        print("get data")

        with MongoDb() as mdb:
            connection = mdb.connection()
            
            for info in connection.find({}):
             
                self.sku_items_list.append(
                    {
                    **info,
                    "path" :   os.path.join(info.get("path")),
                    "created_on" : datetime.strftime(info.get("created_on"), "%H:%M") 
                    } )


    def render(self, sku_id):
        self.current_sku = sku_id
        # self.filtered_items = list(filter(lambda item : item["sku_id"] == sku_id, self.sku_items_list))
        print("render called")
        self.filter("all")
    


    
