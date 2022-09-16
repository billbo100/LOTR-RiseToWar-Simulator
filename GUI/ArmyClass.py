'''
Created on Jun 19, 2022

@author: Culver
'''
from PySide6.QtWidgets import QComboBox, QGridLayout, QLabel,\
    QFrame, QSpinBox, QLineEdit, QTabBar, QWidget, QTabWidget
import pandas as pd
from Commanders.CommanderBase import Commander
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from Unit.Unit import UnitBase
from GUI.EquipmentSelect import EquipmentSelect
from GUI.UnitSelect import UnitSelect
import os
import sys
import logging
class Army(QFrame):
    def __init__(self,title):
        try:
            QFrame.__init__(self)
            self.setFrameStyle(1)
            self.Title=QLabel(title)
            self.CommanderSelect=QComboBox()
            self.CommanderSelect.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.load_Commander_Data()
            
            self.CommanderWidget=Commander()
            
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
                
                
            
            self.equipment=EquipmentSelect()
            self.units=UnitSelect()
            self.tabs=QTabWidget()
            self.tabs.addTab(self.equipment, "Equipment")
            self.tabs.addTab(self.units, "Units")
            self.tabs.addTab(QWidget(), "Abilities")    
                
            self.CommanderWidget.LevelSelect.valueChanged.connect(self.updateCommanderStats)
            self.CommanderWidget.LevelSelect.valueChanged.connect(self.calculateSkillPoints)
            self.CommanderWidget.RespectSelect.valueChanged.connect(self.calculateSkillPoints)    
                
                
                
            self.CommanderWidget.LevelSelect.valueChanged.connect(self.getMaxCommandCount)    
            self.CommanderSelect.currentIndexChanged.connect(self.getMaxCommandCount)
            self.units.Unit1.UnitCount.valueChanged.connect(self.getMaxCommandCount)
            self.units.Unit2.UnitCount.valueChanged.connect(self.getMaxCommandCount)
            self.units.Unit3.UnitCount.valueChanged.connect(self.getMaxCommandCount)
            self.equipment.equipChanged.connect(self.update_Equipment)
            
            self.DamageEstimate=QLabel("FULL DAMAGE ESTIMATE: ")
            self.units.Unit1.dmg_changed.connect(self.update_FULL_DMG)
            self.units.Unit2.dmg_changed.connect(self.update_FULL_DMG)
            self.units.Unit3.dmg_changed.connect(self.update_FULL_DMG)
            
            
            self.CommanderSelect.currentIndexChanged.connect(self.updateCommander)
            self.updateCommander()
            self.getMaxCommandCount()
            
            self.enemy_defense=QSpinBox()
            self.enemy_defense.setMaximum(300)
            self.buffs=QLineEdit()
            self.debuffs=QLineEdit()
            
            self.enemy_defense.valueChanged.connect(self.update_unit_damages)
            self.buffs.textChanged.connect(self.update_unit_damages)
            self.debuffs.textChanged.connect(self.update_unit_damages)
            
            
            
            
            l=QGridLayout()
            l.addWidget(self.Title,0,0)
            l.addWidget(self.CommanderSelect,1,0,1,1)
            l.addWidget(self.CommanderWidget,2,0,1,1)
            l.addWidget(self.tabs,3,0,1,1)
            
            
            
            
            
            
            self.setLayout(l)
        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
            logging.error('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
    def set_commander(self,commander):
        self.Commander=commander
        self.updateCommanderStats()
        self.equipment.weapon.set_commander_restrictions(commander['Race'],self.equipment.Equipment_sort.currentText())
        self.equipment.chest.set_commander_restrictions(commander['Race'],self.equipment.Equipment_sort.currentText())
        self.equipment.head.set_commander_restrictions(commander['Race'],self.equipment.Equipment_sort.currentText())
        self.equipment.accessory.set_commander_restrictions(commander['Race'],self.equipment.Equipment_sort.currentText())
    def updateCommanderStats(self):
        Might=self.calculateMight()
        Focus=self.calculateFocus()
        Speed=self.calculateSpeed()
        self.equipment.sum_equipment_stats()
        Might+=self.equipment.equipment_df["CommanderMight"]
        Focus+=self.equipment.equipment_df["CommanderFocus"]
        Speed+=self.equipment.equipment_df["CommanderSpeed"]
        self.Might=Might
        self.Focus=Focus
        self.Speed=Speed
        self.CommanderWidget.CommanderMight.setText("Might: %d"%(Might))
        self.CommanderWidget.CommanderFocus.setText("Focus: %d"%(Focus))
        self.CommanderWidget.CommanderSpeed.setText("Speed: %d"%(Speed))
    def calculateMight(self):
        lvl=self.CommanderWidget.LevelSelect.value()
        Might=self.Commander.BaseMight
        Might+=lvl*self.Commander.MightScaling
        if(self.Commander.Class=="Balanced" or self.Commander.Class=="Warrior") and (lvl>=20):
            Might+=25
        return Might
    def calculateFocus(self):
        lvl=self.CommanderWidget.LevelSelect.value()
        Focus=self.Commander.BaseFocus
        Focus+=lvl*self.Commander.FocusScaling
        if(self.Commander.Class=="Balanced" or self.Commander.Class=="Strategist") and (lvl>=20):
            Focus+=25
        return Focus
    def calculateSpeed(self):
        lvl=self.CommanderWidget.LevelSelect.value()
        Speed=self.Commander.BaseSpeed
        Speed+=lvl*self.Commander.SpeedScaling
        if(self.Commander.Class=="Balanced") and (lvl>=20):
            Speed+=25
        return Speed
    
    def calculateSkillPoints(self):
        
        lvl=self.CommanderWidget.LevelSelect.value()
        respect=self.CommanderWidget.RespectSelect.value()
        
        SkillPoints=lvl+respect
        if(self.Commander.Class=="Balanced" or self.Commander.Class=="Warrior" or self.Commander.Class=="Strategist") and (lvl>=20):
            SkillPoints+=2
        elif(self.Commander.Class=="Support") and (lvl>=20):
            SkillPoints+=5
        return SkillPoints
    
    
    
    
    
    
    def update_unit_damages(self):
        self.units.Unit1.set_buff_debuff_defense(self.enemy_defense.value(),self.buffs.text()+',%.3f'%(self.CommanderWidget.Might/2000),self.debuffs.text())
        self.units.Unit2.set_buff_debuff_defense(self.enemy_defense.value(),self.buffs.text()+',%.3f'%(self.CommanderWidget.Might/2000),self.debuffs.text())
        self.units.Unit3.set_buff_debuff_defense(self.enemy_defense.value(),self.buffs.text()+',%.3f'%(self.CommanderWidget.Might/2000),self.debuffs.text())
    def update_FULL_DMG(self):
        min_damages=self.units.Unit1.min_estimate+self.units.Unit2.min_estimate+self.units.Unit3.min_estimate
        max_damages=self.units.Unit1.max_estimate+self.units.Unit2.max_estimate+self.units.Unit3.max_estimate
        self.DamageEstimate.setText("FULL DAMAGE ESTIMATE: %d-%d"%(min_damages,max_damages))
    def update_Equipment(self):
        self.updateCommanderStats()
        self.units.Unit1.updateEquipment(self.equipment.equipment_df)
        self.units.Unit2.updateEquipment(self.equipment.equipment_df)
        self.units.Unit3.updateEquipment(self.equipment.equipment_df)
    def getMaxCommandCount(self):
        self.max_command=25
        self.max_command+=self.CommanderWidget.LevelSelect.value()
        if(self.Commander["Class"]=="Leader" and self.CommanderWidget.LevelSelect.value()>=20):
            self.max_command+=5
            
        Unit1Max=self.max_command-self.units.Unit2.currentCommands-self.units.Unit3.currentCommands
        Unit2Max=self.max_command-self.units.Unit1.currentCommands-self.units.Unit3.currentCommands
        Unit3Max=self.max_command-self.units.Unit1.currentCommands-self.units.Unit2.currentCommands
        self.units.Unit1.setMaxCommand(Unit1Max)
        self.units.Unit2.setMaxCommand(Unit2Max)
        self.units.Unit3.setMaxCommand(Unit3Max)
    def load_Commander_Data(self):
        self.commander_DF=pd.read_csv("data/Commanders.csv",index_col="Commander")


    def updateCommander(self):
        commander=self.commander_DF.loc[self.CommanderSelect.currentText()]
        self.set_commander(commander)
        if(commander["Side"]=="Good"):
            color='rgb(144,238,144)'
        else:
            color='rgb(255,144,144)'
        self.CommanderSelect.setStyleSheet("QPushButton{background-color : %s;}"%color)
        self.CommanderSelect.setStyleSheet('QComboBox{selection-border-color: rgb(0,0,0);}')
        
        
        
        
        
        