'''
Created on Jun 19, 2022

@author: Culver
'''
from PySide2.QtWidgets import QWidget, QComboBox, QSpinBox, QGridLayout, QLabel
import pandas as pd
class Commander(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
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
        self.LevelSelect.valueChanged.connect(self.updateCommanderStats)
        self.LevelSelect.valueChanged.connect(self.calculateSkillPoints)
        self.RespectSelect.valueChanged.connect(self.calculateSkillPoints)
        l=QGridLayout()
        l.addWidget(self.LevelLabel,0,0)
        l.addWidget(self.RespectLabel,0,2)
        l.addWidget(self.LevelSelect,0,1)
        l.addWidget(self.RespectSelect,0,3)
        l.addWidget(self.CommanderMight,1,0)
        l.addWidget(self.CommanderFocus,1,1)
        l.addWidget(self.CommanderSpeed,1,2)
        self.setLayout(l)
        
    def set_commander(self,commander):
        self.Commander=commander
        self.updateCommanderStats()
    def updateCommanderStats(self):
        Might=self.calculateMight()
        Focus=self.calculateFocus()
        Speed=self.calculateSpeed()
        self.CommanderMight.setText("Might: %d"%(Might))
        self.CommanderFocus.setText("Focus: %d"%(Focus))
        self.CommanderSpeed.setText("Speed: %d"%(Speed))
    def calculateMight(self):
        lvl=self.LevelSelect.value()
        Might=self.Commander.BaseMight
        Might+=lvl*self.Commander.MightScaling
        if(self.Commander.Class=="Balanced" or self.Commander.Class=="Warrior") and (lvl>=20):
            Might+=25
        return Might
    def calculateFocus(self):
        lvl=self.LevelSelect.value()
        Focus=self.Commander.BaseFocus
        Focus+=lvl*self.Commander.FocusScaling
        if(self.Commander.Class=="Balanced" or self.Commander.Class=="Strategist") and (lvl>=20):
            Focus+=25
        return Focus
    def calculateSpeed(self):
        lvl=self.LevelSelect.value()
        Speed=self.Commander.BaseSpeed
        Speed+=lvl*self.Commander.SpeedScaling
        if(self.Commander.Class=="Balanced") and (lvl>=20):
            Speed+=25
        return Speed


    def calculateSkillPoints(self):
        
        lvl=self.LevelSelect.value()
        respect=self.RespectSelect.value()
        
        SkillPoints=lvl+respect
        if(self.Commander.Class=="Balanced" or self.Commander.Class=="Warrior" or self.Commander.Class=="Strategist") and (lvl>=20):
            SkillPoints+=2
        elif(self.Commander.Class=="Support") and (lvl>=20):
            SkillPoints+=5
        return SkillPoints


