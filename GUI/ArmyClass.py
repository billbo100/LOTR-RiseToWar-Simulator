'''
Created on Jun 19, 2022

@author: Culver
'''
from PySide2.QtWidgets import QWidget, QComboBox, QSpinBox, QGridLayout, QLabel,\
    QFrame
import pandas as pd
from Commanders.CommanderBase import Commander
from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QColor
class Army(QFrame):
    def __init__(self,title):
        QFrame.__init__(self)
        self.setFrameStyle(1)
        self.Title=QLabel(title)
        
        self.CommanderSelect=QComboBox()
        self.CommanderSelect.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.load_Commander_Data()
        
        self.CommanderWidget=Commander()
        self.CommanderSelect.currentIndexChanged.connect(self.updateCommander)
        self.CommanderSelect.addItems(self.commander_DF.index.sort_values())
        self.CommanderSelect.setStyleSheet('selection-background-color: rgba(0,0,0,0)')
        self.CommanderSelect.setStyleSheet('QComboBox{selection-border-color: rgb(0,0,0);}')
        for i in range(self.CommanderSelect.count()):
            commander=self.commander_DF.loc[self.CommanderSelect.itemText(i)]
            if(commander["Side"]=="Good"):
                color=QColor(144,238,144)
            else:
                color=QColor(255,144,144)
            self.CommanderSelect.model().item(i).setBackground(color)
            # print(self.CommanderSelect.model().item(i).background())
        l=QGridLayout()
        l.addWidget(self.Title,0,0)
        l.addWidget(self.CommanderSelect,1,0)
        l.addWidget(self.CommanderWidget,2,0)
        self.setLayout(l)
        
    def load_Commander_Data(self):
        self.commander_DF=pd.read_csv("Commanders.csv",index_col="Commander")


    def updateCommander(self):
        commander=self.commander_DF.loc[self.CommanderSelect.currentText()]
        self.CommanderWidget.set_commander(commander)
        if(commander["Side"]=="Good"):
            color='rgb(144,238,144)'
        else:
            color='rgb(255,144,144)'
        self.CommanderSelect.setStyleSheet("QPushButton{background-color : %s;}"%color)
        self.CommanderSelect.setStyleSheet('QComboBox{selection-border-color: rgb(0,0,0);}')