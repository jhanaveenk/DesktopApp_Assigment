from PySide2.QtWidgets import QApplication, QStackedLayout, QLabel, QPushButton, QBoxLayout, QWidget, QMainWindow, QTabWidget, QVBoxLayout, QFrame
from PySide2.QtCore import QSize, Qt

import sys
from ui.components.molecules.tab.tabs import Tabs
from ui.components.molecules.tab.tab import Tab
from controllers.imagePanelController import ImageGalleryPanel
from controllers.analyticsPanelController import AnalyticsPanel
from model.setup import MongoDb
import os
import numpy as np
from PIL import Image
import shutil
from datetime import datetime, timedelta
from random import randint
from ui.components.molecules.loader.loader import Loader

ASSETS_FILE_PATH = os.path.join("./assets/")


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Switchon assignment")
        self.resize(1000, 900)
        self._sku_list = list()
        self._filtered_sku = list()
        self._current_sku = 1
        self.is_loading = 0
        self.main_widget = QWidget()
        self.container = QVBoxLayout(self.main_widget)
        self.setCentralWidget(self.main_widget)
        # self.setCentralWidget(self.loader)
        # self.load_data()
        self.loader = Loader()
        self.__get_data()
        
        self.add_tabs()
        # self._filter_skus()

    def show_loader(self):
        if self.loader.isVisible():
            self.loader.hide()
        else:
            self.loader.show()

    def add_tabs(self):
        self.tabs = Tabs()
        self.tabs.addTab( u"Analytics")
        self.tabs.addTab( u"Image Gallery")
 
        self.tabs.setStyleSheet("""

            QTabBar::tear {

                border-color : red;
            }

               

            QTabBar::tab {
                min-width: 1ex;
                min-height : 4ex;
                padding: 2px;
                border : 2px solid #303135b8;
                border-top-left-radius : 5px;
                border-top-right-radius : 5px;
                margin-left : 4px;
    
            }

            QTabBar::tab:selected, QTabBar::tab:hover {
                background : #f4f5f6ed;
            }

            QTabBar::tab:selected {
                background : transparent;
                border-bottom-color : transparent;
            }

            QTabBar::tab:!selected {
                background : #f4f5f6ed;
            }
        """)
        # binding signals to handlers

        self.tabs.currentChanged.connect(self.handle_tab_click)
        self.tab_panel = QFrame(self.main_widget)
        # self.tab_panel.setStyleSheet("""" background : white; """)
        self.tab_panel.setObjectName(u"tabPanel")
        # self.tab_panel.setMaximumSize(QSize(500, 600))
        self.tab_panel.setFrameShape(QFrame.NoFrame)
        self.tab_panel_layout = QStackedLayout(self.tab_panel)

        self.panel1 = AnalyticsPanel(self)
        self.panel2 = ImageGalleryPanel(self)
        self.current_panel = self.panel1

        self.tab_panel_layout.addWidget(self.panel1)
        self.tab_panel_layout.addWidget(self.panel2)

        self.tab_panel_layout.setCurrentIndex(0)

        self.container.addWidget(self.tabs)
        self.container.addWidget(self.tab_panel)
        pass

    def _filter_skus(self):
        print("current sku", self._current_sku, len(self._sku_list))

        self._filtered_sku = list(filter(lambda item: item.get(
            "sku_id") == self._current_sku,  self._sku_list))
        print("self._filtered_sku -- ", len(self._filtered_sku))

        try:
            self.panel2.render(self._current_sku)
        except Exception as e:
            print(e)

    def __get_data(self):

        with MongoDb() as mdb:
            connection = mdb.connection()
            for info in connection.find({}):

                self._sku_list.append(
                    {
                        **info,
                        "path":   os.path.join(info.get("path")),
                        "created_on": datetime.strftime(info.get("created_on"), "%H:%M")
                    })
        self._filter_skus()
        # self.show_loader()

    # def clear_panel(self):
    #     try:
    #         while ((child := self.selectedPanel.takeAt(0)) != None):
    #             child.widget().deleteLater()
    #     except Exception as e :
    #         print(e)

    def handle_tab_click(self, currentIndex, *args, **kwargs):
        # self.clear_panel()
        if currentIndex == 1:
            # self.selectedPanel.removeWidget(self.currentPanel)
            self.tab_panel_layout.setCurrentIndex(currentIndex)
            self.current_panel = self.panel2
        else:
            self.tab_panel_layout.setCurrentIndex(currentIndex)
            self.current_panel = self.panel1

    @classmethod
    def __populate_db(cls, current_sku, item_id, con, bad_image, good_image):
        rv = np.random.choice(np.arange(0, 2), p=[0.3, 0.7])
        product_image_path = None
        img = None
        parent_dir = f"sku{current_sku}"
        if rv:
            img = Image.open(os.path.join(ASSETS_FILE_PATH, good_image))
            product_image_path = os.path.join(
                ASSETS_FILE_PATH, f"{parent_dir}/good/{item_id}.jpg")
        else:
            img = Image.open(os.path.join(ASSETS_FILE_PATH, bad_image))
            product_image_path = os.path.join(
                ASSETS_FILE_PATH, f"{parent_dir}/bad/{item_id}.jpg")

        img.save(product_image_path)
        timestamp = [datetime(2023, 10, 2, 8, 10), datetime(2023, 10, 2, 9, 10), datetime(
            2023, 10, 2, 10, 10), datetime(2023, 10, 2, 11, 10)]
        payload = {
            "sku_id": current_sku,
            "unit_id": item_id,
            "status": "good" if rv else "bad",
            "path": product_image_path,
            "created_on": timestamp[randint(0, 3)]

        }
        con.insert_one(payload)

    def _set_current_sku(self, type, *args, **kwargs):
        self._current_sku = type

    @classmethod
    def load_data(cls, sku=1, bimg="bottlebad.jpg", gimg="bottlegood.webp"):
        parent_dir = f"sku{sku}"

        try:
            shutil.rmtree(os.path.join(ASSETS_FILE_PATH, f"{parent_dir}"))
        except Exception as e:
            print(e)

        os.mkdir(os.path.join(ASSETS_FILE_PATH, f"{parent_dir}"))

        os.mkdir(os.path.join(ASSETS_FILE_PATH, f"{parent_dir}/good"))
        os.mkdir(os.path.join(ASSETS_FILE_PATH, f"{parent_dir}/bad"))

        with MongoDb() as mdb:
            con = mdb.connection()
            # with ThreadPoolExecutor(10) as executor:
            #     futures = [ executor.submit(self.__populate_db, id, con) for id in range(total_no_of_img) ]
            #     wait(futures)
            # for row in range(10):
            #     for col in range(5):
            #         image = ImageFrame(self.sku_items_list[(row+col)%10], 150, 100)
            #         self.grid_layout.addWidget(image, row, col)

            for id in range(100):
                cls.__populate_db(sku, int(id), con, bimg, gimg)


if __name__ == '__main__':

    if "load" in sys.argv:
        MainWindow.load_data()
        MainWindow.load_data(2, "capbad.jpg", "capgood.jpg")
    else:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
