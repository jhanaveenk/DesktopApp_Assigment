from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QTabBar

class Tabs(QTabBar):

    def __init__(self):
        super(Tabs, self).__init__()
        self.setMaximumWidth(400)
        
    
