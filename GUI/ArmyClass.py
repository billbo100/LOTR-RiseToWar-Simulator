'''
Created on Jun 19, 2022

@author: Culver
'''
from PySide2.QtWidgets import QWidget, QComboBox, QSpinBox, QGridLayout, QLabel
import pandas as pd
from Commanders.CommanderBase import Commander
from PySide2.QtCore import Qt
class Army(QWidget):
    def __init__(self,title):
        QWidget.__init__(self)
        self.Title=QLabel(title)
        
        self.CommanderSelect=QComboBox()
        self.CommanderSelect.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.load_Commander_Data()
        
        self.CommanderWidget=Commander()
        self.CommanderSelect.currentIndexChanged.connect(self.updateCommander)
        self.CommanderSelect.addItems(self.commander_DF.index.sort_values())
        l=QGridLayout()
        l.addWidget(self.Title,0,0)
        l.addWidget(self.CommanderSelect,1,0)
        l.addWidget(self.CommanderWidget,2,0)
        self.setLayout(l)
        
    def load_Commander_Data(self):
        self.commander_DF=pd.read_csv("Commanders.csv",index_col="Commander")


    def updateCommander(self):
        self.CommanderWidget.set_commander(self.commander_DF.loc[self.CommanderSelect.currentText()])