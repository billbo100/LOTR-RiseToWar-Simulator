'''
Created on Jun 19, 2022

@author: Culver
'''
from PySide2.QtWidgets import QWidget, QComboBox, QSpinBox, QGridLayout, QLabel
import pandas as pd
class Army(QWidget):
    def __init__(self,title):
        QWidget.__init__(self)
        self.Title=QLabel(title)
        
        self.CommanderSelect=QComboBox()
        self.load_Commander_Data()
        
        self.LevelLabel=QLabel("Level")
        self.LevelSelect=QSpinBox()
        self.LevelSelect.setMinimum(0)
        self.LevelSelect.setMaximum(50)
        
        self.RespectLabel=QLabel("Respect")
        self.RespectSelect=QSpinBox()
        self.RespectSelect.setMinimum(0)
        self.RespectSelect.setMaximum(25)
        
        self.CommanderMight=QLabel("Might:")
        self.CommanderFocus=QLabel("Focus:")
        self.CommanderSpeed=QLabel("Speed:")
        self.CommanderSelect.currentIndexChanged.connect(self.updateCommanderStats)
        self.CommanderSelect.addItems(self.commander_DF.index.sort_values())
        self.LevelSelect.valueChanged.connect(self.updateCommanderStats)
        
        l=QGridLayout()
        l.addWidget(self.Title,0,0)
        l.addWidget(self.LevelLabel,0,1)
        l.addWidget(self.RespectLabel,0,2)
        l.addWidget(self.CommanderSelect,1,0)
        l.addWidget(self.LevelSelect,1,1)
        l.addWidget(self.RespectSelect,1,2)
        l.addWidget(self.CommanderMight,2,0)
        l.addWidget(self.CommanderFocus,2,1)
        l.addWidget(self.CommanderSpeed,2,2)
        self.setLayout(l)
        
    def load_Commander_Data(self):
        self.commander_DF=pd.read_csv("Commanders.csv",index_col="Commander")
        print(self.commander_DF)


    def updateCommanderStats(self):
        pass
        comm=self.commander_DF.loc[self.CommanderSelect.currentText()]
        lvl=self.LevelSelect.value()
        Might=self.calculateMight()
        Focus=self.calculateFocus()
        Speed=self.calculateSpeed()
        self.CommanderMight.setText("Might: %d"%(Might))
        self.CommanderFocus.setText("Focus: %d"%(Focus))
        self.CommanderSpeed.setText("Speed: %d"%(Speed))
    def calculateMight(self):
        comm=self.commander_DF.loc[self.CommanderSelect.currentText()]
        lvl=self.LevelSelect.value()
        Might=comm.BaseMight
        Might+=lvl*comm.MightScaling
        if(comm.Class=="Balanced" or comm.Class=="Warrior") and (lvl>=20):
            Might+=25
        return Might
    def calculateFocus(self):
        comm=self.commander_DF.loc[self.CommanderSelect.currentText()]
        lvl=self.LevelSelect.value()
        Focus=comm.BaseFocus
        Focus+=lvl*comm.FocusScaling
        if(comm.Class=="Balanced" or comm.Class=="Strategist") and (lvl>=20):
            Focus+=25
        return Focus
    def calculateSpeed(self):
        comm=self.commander_DF.loc[self.CommanderSelect.currentText()]
        lvl=self.LevelSelect.value()
        Speed=comm.BaseSpeed
        Speed+=lvl*comm.SpeedScaling
        if(comm.Class=="Balanced") and (lvl>=20):
            Speed+=25
        return Speed







