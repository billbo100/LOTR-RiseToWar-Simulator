'''
Created on Jun 19, 2022

@author: Culver
'''
from PySide2.QtWidgets import QWidget, QComboBox, QSpinBox, QGridLayout, QLabel
import pandas as pd
from Equipment.Equipment import EquipmentBase
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
        self.load_Equipment()
        self.Equipment_sort=QComboBox()
        all_vals=list(self.Equipment_DF.columns)
        non_sortable=["EquipmentType","Maiar","Men","Elves","Dwarves","Undead","Evil Men","Ents","Orcs","Uruk-hai","Hobbits"]
        sortable_vals=[x for x in all_vals if (not x in non_sortable)]
        self.Equipment_sort.addItems(sortable_vals)
        self.Equipment_sort.currentIndexChanged.connect(self.set_update_equipment_sorting)
        
        self.weapon=EquipmentBase(self.Equipment_DF[self.Equipment_DF["EquipmentType"]=="Weapon"])
        self.weapon.itemSelect.currentIndexChanged.connect(self.updateCommanderStats)
        self.weapon.strengthenSelect.valueChanged.connect(self.updateCommanderStats)
        
        self.chest=EquipmentBase(self.Equipment_DF[self.Equipment_DF["EquipmentType"]=="Armor"])
        self.chest.itemSelect.currentIndexChanged.connect(self.updateCommanderStats)
        self.chest.strengthenSelect.valueChanged.connect(self.updateCommanderStats)
        
        self.head=EquipmentBase(self.Equipment_DF[self.Equipment_DF["EquipmentType"]=="Helmet"])
        self.head.itemSelect.currentIndexChanged.connect(self.updateCommanderStats)
        self.head.strengthenSelect.valueChanged.connect(self.updateCommanderStats)
        
        self.accessory=EquipmentBase(self.Equipment_DF[self.Equipment_DF["EquipmentType"]=="Accessory"])
        self.accessory.itemSelect.currentIndexChanged.connect(self.updateCommanderStats)
        self.accessory.strengthenSelect.valueChanged.connect(self.updateCommanderStats)
        
        
        l=QGridLayout()
        l.addWidget(self.LevelLabel,0,0)
        l.addWidget(self.RespectLabel,0,2)
        l.addWidget(self.LevelSelect,0,1)
        l.addWidget(self.RespectSelect,0,3)
        l.addWidget(self.CommanderMight,1,0)
        l.addWidget(self.CommanderFocus,1,1)
        l.addWidget(self.CommanderSpeed,1,2)
        l.addWidget(self.Equipment_sort,1,3)
        l.addWidget(self.weapon,2,0)
        l.addWidget(self.chest,2,1)
        l.addWidget(self.head,2,2)
        l.addWidget(self.accessory,2,3)
        self.setLayout(l)
    def load_Equipment(self):
        self.Equipment_DF=pd.read_csv("EquipmentFull.csv",index_col="Name")
        
    def get_equipment_stats(self):
        
        wm,wf,ws=self.weapon.get_stats()
        sm,sf,ss=self.chest.get_stats()
        hm,hf,hs=self.head.get_stats()
        hm,hf,hs=self.head.get_stats()
        am,af,a_s=self.accessory.get_stats()
        m=wm+sm+hm+am
        f=wf+sf+hf+af
        s=wf+ss+hs+a_s
        return m,f,s
    def set_commander(self,commander):
        self.Commander=commander
        self.updateCommanderStats()
        self.weapon.set_commander_restrictions(commander['Race'],self.Equipment_sort.currentText())
        self.chest.set_commander_restrictions(commander['Race'],self.Equipment_sort.currentText())
        self.head.set_commander_restrictions(commander['Race'],self.Equipment_sort.currentText())
        self.accessory.set_commander_restrictions(commander['Race'],self.Equipment_sort.currentText())
    def set_update_equipment_sorting(self):
        self.weapon.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
        self.chest.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
        self.head.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
        self.accessory.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
    def updateCommanderStats(self):
        Might=self.calculateMight()
        Focus=self.calculateFocus()
        Speed=self.calculateSpeed()
        m,f,s=self.get_equipment_stats()
        Might+=m
        Focus+=f
        Speed+=s
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


