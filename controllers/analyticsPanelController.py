from PySide2.QtWidgets import QApplication, QComboBox, QMenuBar, QMenu, QPushButton, QFrame,  QWidget, QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout
from PySide2.QtCore import QSize, Qt
import sys

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

class PlotSku(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PlotSku, self).__init__(fig)



class AnalyticsPanel(QWidget):

    def __init__(self,parent, *args, **kwargs):
        super(AnalyticsPanel, self).__init__(*args, **kwargs)
        self.parent = parent        
        self._layout = QVBoxLayout(self)

        self.row1_widget = QWidget(self)
        self.row1_layout = QHBoxLayout(self.row1_widget)
        self.row1_widget.setStyleSheet( """ 
        """)
        self.row1_widget.setMaximumSize(100, 30)
        self._layout.addWidget(self.row1_widget)
        self.row2_widget = QWidget(self)
        self.row2_layout = QHBoxLayout(self.row2_widget)
        self._layout.addWidget(self.row2_widget)

        self.row2_widget.setStyleSheet("""
        """)
        self.menu_box = QComboBox(self.row1_widget)
        self.menu_box.addItems(["SKU1", "SKU2"])
        self.menu_box.currentIndexChanged.connect( lambda index : self.handle_menu_index_change(index) )

        self.chart_widget = PlotSku(self.row2_layout,  dpi=100)
        self.chart_widget.setStyleSheet("""
            background : black;
        """)
        # self.chart_widget.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        self.sku_list = self.parent._sku_list
        self.filtered_skus_list = self.parent._filtered_sku
        self.current_sku = self.parent._current_sku
        self.set_current_sku = self.parent._set_current_sku
        self.filter_skus = self.parent._filter_skus
        self.show_loader = self.parent.show_loader
        self.plot_graph()
        self.row2_layout.addWidget(self.chart_widget)


    def update_plot(self):

        # Drop off the first y element, append a new one.
        self.chart_widget.axes.cla()  # Clear the canvas.
        self.plot_graph()
        self.chart_widget.draw()


    def render(self, sku_id):
        self.__get_data()
        self.filtered_skus_list = list(filter(lambda item : item.get("sku_id") == sku_id, self.sku_list))
        self.update_plot()

    def __get_data(self):

        self.show_loader()
        with MongoDb() as mdb:
            connection = mdb.connection()
            data = list()
            for info in connection.find({}):
             
                data.append(
                    {
                    **info,
                    "path" :   os.path.join(info.get("path")),
                    "created_on" : datetime.strftime(info.get("created_on"), "%H:%M") 
                    } )
            self.sku_list = tuple(data)
        self.show_loader()
        i = 0

    def plot_graph(self):
        count_bad_sku = len(list(filter(lambda x : x.get("status") == "bad" , self.filtered_skus_list) ))
        count_good_sku = len(list(filter(lambda x : x.get("status") == "good" , self.filtered_skus_list) ))
        if len(self.filtered_skus_list) == 0:
            return
        
        label_dict = dict()
        print(self.filtered_skus_list[:2])
        for item in self.filtered_skus_list:
            if label_dict.get(item.get("created_on"), False):
                label_dict[item.get("created_on")][item.get("status")] += 1
            else:
                label_dict[item.get("created_on")] = { "bad" : 0 , "good" : 0}
                label_dict[item.get("created_on")][item.get("status")] += 1


        # print(label_dict.items() ) 
        N = len(label_dict.items())
        bad_sku = tuple(map(lambda item : item[1].get("bad"), label_dict.items()))
        good_sku = tuple(map(lambda item : item[1].get("good"), label_dict.items()))
        # print(len(bad_sku), len(good_sku))
        # badStd = (1, 2, 3)
        # goodStd = (1, 2, 3)
        ind = np.arange(N)
        width = 0.30

        fig = self.chart_widget.axes.plot(figsize =(10, 7))
        p2 = self.chart_widget.axes.bar(ind, bad_sku, width)
        p1 = self.chart_widget.axes.bar(ind, good_sku, width, bottom = bad_sku)

        # self.chart_widget.axes.yl ('Contribution')
        # self.chart_widget.axes.title('Contribution by the teams')
        self.chart_widget.axes.set_xticks(ind, tuple( map(lambda item : item[0], label_dict.items())) )
        # self.chart_widget.axes.set_yticks(np.arange(0, 81, 10))
        self.chart_widget.axes.legend((p1[0], p2[0]), ('good', 'bad'))



    def handle_menu_index_change(self, current_index, *args, **kwargs):
        self.set_current_sku(current_index+1)
        # print(self.parent().current_sku)
        self.filter_skus()
        # print("self.parent._sku_list",self.parent._sku_list)
        self.render(current_index + 1)



    