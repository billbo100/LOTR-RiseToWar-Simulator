'''
Created on Jun 19, 2022

@author: Culver
'''
from PySide2.QtWidgets import QComboBox, QGridLayout, QLabel,\
    QFrame, QSpinBox, QLineEdit
import pandas as pd
from Commanders.CommanderBase import Commander
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QFont
import Unit
from Unit.Unit import UnitBase
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
        self.CommanderSelect.setFont(QFont("Arial",16))    
            
            
        self.Unit1=UnitBase()
        self.Unit2=UnitBase()
        self.Unit3=UnitBase()
            
            
            
            
            
            
        self.CommanderWidget.LevelSelect.valueChanged.connect(self.getMaxCommandCount)    
        self.CommanderSelect.currentIndexChanged.connect(self.getMaxCommandCount)
        self.Unit1.UnitCount.valueChanged.connect(self.getMaxCommandCount)
        self.Unit2.UnitCount.valueChanged.connect(self.getMaxCommandCount)
        self.Unit3.UnitCount.valueChanged.connect(self.getMaxCommandCount)
        self.CommanderWidget.equipChanged.connect(self.update_Equipment)
        
        self.DamageEstimate=QLabel("FULL DAMAGE ESTIMATE: ")
        self.Unit1.dmg_changed.connect(self.update_FULL_DMG)
        self.Unit2.dmg_changed.connect(self.update_FULL_DMG)
        self.Unit3.dmg_changed.connect(self.update_FULL_DMG)
        
        
        self.enemy_defense=QSpinBox()
        self.enemy_defense.setMaximum(300)
        self.buffs=QLineEdit()
        self.debuffs=QLineEdit()
        
        self.enemy_defense.valueChanged.connect(self.update_unit_damages)
        self.buffs.textChanged.connect(self.update_unit_damages)
        self.debuffs.textChanged.connect(self.update_unit_damages)
        
        
        
        
        self.getMaxCommandCount()
        
        l=QGridLayout()
        l.addWidget(self.Title,0,0)
        l.addWidget(self.CommanderSelect,1,0,1,1)
        l.addWidget(self.CommanderWidget,2,0,1,3)
        l.addWidget(self.Unit1,3,0,1,1)
        l.addWidget(self.Unit2,3,1,1,1)
        l.addWidget(self.Unit3,3,2,1,1)
        
        
        l.addWidget(self.enemy_defense,4,0,1,3)
        l.addWidget(self.buffs,5,0,1,3)
        l.addWidget(self.debuffs,6,0,1,3)
        l.addWidget(self.DamageEstimate,7,0,1,3)
        self.setLayout(l)
    def update_unit_damages(self):
        self.Unit1.set_buff_debuff_defense(self.enemy_defense.value(),self.buffs.text()+',%.3f'%(self.CommanderWidget.Might/2000),self.debuffs.text())
        self.Unit2.set_buff_debuff_defense(self.enemy_defense.value(),self.buffs.text()+',%.3f'%(self.CommanderWidget.Might/2000),self.debuffs.text())
        self.Unit3.set_buff_debuff_defense(self.enemy_defense.value(),self.buffs.text()+',%.3f'%(self.CommanderWidget.Might/2000),self.debuffs.text())
    def update_FULL_DMG(self):
        min_damages=self.Unit1.min_estimate+self.Unit2.min_estimate+self.Unit3.min_estimate
        max_damages=self.Unit1.max_estimate+self.Unit2.max_estimate+self.Unit3.max_estimate
        self.DamageEstimate.setText("FULL DAMAGE ESTIMATE: %d-%d"%(min_damages,max_damages))
    def update_Equipment(self):
        self.Unit1.updateEquipment(self.CommanderWidget.equipment_df)
        self.Unit2.updateEquipment(self.CommanderWidget.equipment_df)
        self.Unit3.updateEquipment(self.CommanderWidget.equipment_df)
    def getMaxCommandCount(self):
        self.max_command=25
        self.max_command+=self.CommanderWidget.LevelSelect.value()
        if(self.CommanderWidget.Commander["Class"]=="Leader" and self.CommanderWidget.LevelSelect.value()>=20):
            self.max_command+=5
            
        Unit1Max=self.max_command-self.Unit2.currentCommands-self.Unit3.currentCommands
        Unit2Max=self.max_command-self.Unit1.currentCommands-self.Unit3.currentCommands
        Unit3Max=self.max_command-self.Unit1.currentCommands-self.Unit2.currentCommands
        self.Unit1.setMaxCommand(Unit1Max)
        self.Unit2.setMaxCommand(Unit2Max)
        self.Unit3.setMaxCommand(Unit3Max)
    def load_Commander_Data(self):
        self.commander_DF=pd.read_csv("data/Commanders.csv",index_col="Commander")


    def updateCommander(self):
        commander=self.commander_DF.loc[self.CommanderSelect.currentText()]
        self.CommanderWidget.set_commander(commander)
        if(commander["Side"]=="Good"):
            color='rgb(144,238,144)'
        else:
            color='rgb(255,144,144)'
        self.CommanderSelect.setStyleSheet("QPushButton{background-color : %s;}"%color)
        self.CommanderSelect.setStyleSheet('QComboBox{selection-border-color: rgb(0,0,0);}')
        
        
        
        
        
        