'''
Created on Jun 19, 2022

@author: Culver
'''
from PySide6.QtWidgets import QWidget, QComboBox, QSpinBox, QGridLayout, QLabel
import pandas as pd
from Equipment.Equipment import EquipmentBase
from PySide6.QtCore import Signal
class Commander(QWidget):
    
    def __init__(self):
        QWidget.__init__(self)
        
        self.LevelLabel=QLabel("Level")
        self.LevelSelect=QSpinBox()
        self.LevelSelect.setMinimum(1)
        self.LevelSelect.setMaximum(50)
        
        self.RespectLabel=QLabel("Respect")
        self.RespectSelect=QSpinBox()
        self.RespectSelect.setMinimum(0)
        self.RespectSelect.setMaximum(25)
        
        
        self.CommanderMight=QLabel("Might:")
        self.CommanderFocus=QLabel("Focus:")
        self.CommanderSpeed=QLabel("Speed:")

        l=QGridLayout()
        l.addWidget(self.LevelLabel,0,0)
        l.addWidget(self.RespectLabel,0,2)
        l.addWidget(self.LevelSelect,0,1)
        l.addWidget(self.RespectSelect,0,3)
        l.addWidget(self.CommanderMight,1,0)
        l.addWidget(self.CommanderFocus,1,1)
        l.addWidget(self.CommanderSpeed,1,2)
        self.setLayout(l)
        
        
        
    
    def set_update_equipment_sorting(self):
        self.weapon.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
        self.chest.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
        self.head.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
        self.accessory.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())

