'''
Created on Jun 19, 2022

@author: Culver
'''
from PySide2.QtWidgets import QWidget, QComboBox, QSpinBox, QGridLayout, QLabel
import pandas as pd
from Equipment.Equipment import EquipmentBase
from PySide2.QtCore import Signal
class Commander(QWidget):
    equipChanged=Signal()
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
        self.LevelSelect.valueChanged.connect(self.updateCommanderStats)
        self.LevelSelect.valueChanged.connect(self.calculateSkillPoints)
        self.RespectSelect.valueChanged.connect(self.calculateSkillPoints)
        self.load_Equipment()
        self.Equipment_sort=QComboBox()
        all_vals=list(self.full_Equipment_DF.columns)
        non_sortable=["EquipmentType","Maiar","Men","Elves","Dwarves","Undead","Evil Men","Ents","Orcs","Uruk-hai","Hobbits","Chest","Perks"]
        sortable_vals=[x for x in all_vals if (not x in non_sortable)]
        self.Equipment_sort.addItems(sortable_vals)
        self.Equipment_sort.currentIndexChanged.connect(self.set_update_equipment_sorting)
        
        self.weapon=EquipmentBase(self.full_Equipment_DF[self.full_Equipment_DF["EquipmentType"]=="Weapon"],self.perk_DF)
        self.weapon.itemSelect.currentIndexChanged.connect(self.updateCommanderStats)
        self.weapon.strengthenSelect.valueChanged.connect(self.updateCommanderStats)
        self.weapon.refinementSelect.valueChanged.connect(self.updateCommanderStats)
        
        self.chest=EquipmentBase(self.full_Equipment_DF[self.full_Equipment_DF["EquipmentType"]=="Armor"],self.perk_DF)
        self.chest.itemSelect.currentIndexChanged.connect(self.updateCommanderStats)
        self.chest.strengthenSelect.valueChanged.connect(self.updateCommanderStats)
        self.chest.refinementSelect.valueChanged.connect(self.updateCommanderStats)
        
        self.head=EquipmentBase(self.full_Equipment_DF[self.full_Equipment_DF["EquipmentType"]=="Helmet"],self.perk_DF)
        self.head.itemSelect.currentIndexChanged.connect(self.updateCommanderStats)
        self.head.strengthenSelect.valueChanged.connect(self.updateCommanderStats)
        self.head.refinementSelect.valueChanged.connect(self.updateCommanderStats)
        
        self.accessory=EquipmentBase(self.full_Equipment_DF[self.full_Equipment_DF["EquipmentType"]=="Accessory"],self.perk_DF)
        self.accessory.itemSelect.currentIndexChanged.connect(self.updateCommanderStats)
        self.accessory.strengthenSelect.valueChanged.connect(self.updateCommanderStats)
        self.accessory.refinementSelect.valueChanged.connect(self.updateCommanderStats)
        
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
        self.full_Equipment_DF=pd.read_csv("data/EquipmentFull.csv",index_col="Name")
        self.perk_DF=pd.read_csv("data/EquipPerkProccessed.csv",index_col="Name")
    def reset_equipment_df(self):
        blank_equips={ 'Rarity':0,'Name':'','CommanderMight':0,'CommanderFocus':0, 'CommanderSpeed':0,'Attack(ALL)':0, 
                       'Attack(Beasts)':0, 'Attack(Dwarves)':0, 'Attack(Elves)':0,
                       'Attack(Evil Men)':0, 'Attack(Hobbits)':0, 'Attack(Large Units)':0,
                       'Attack(Melee)':0, 'Attack(Men)':0, 'Attack(Mounted Units)':0, 'Attack(Orcs)':0,
                       'Attack(Ranged)':0, 'Attack(Trolls)':0, 'Attack(Undead)':0,
                       'Attack(Uruk-Hai)':0, 'Attack(Uruk-hai)':0, 'Chest':0, 'Defense(ALL)':0, 'Defense(Beasts)':0,
                       'Defense(Dwarves)':0, 'Defense(Elves)':0, 'Defense(Evil Men)':0,
                       'Defense(Hobbits)':0, 'Defense(Large Units)':0, 'Defense(Melee)':0,
                       'Defense(Men)':0, 'Defense(Mounted Units)':0, 'Defense(Orcs)':0,
                       'Defense(Ranged)':0, 'Defense(Trolls)':0, 'Defense(Undead)':0,
                       'Defense(Uruk-Hai)':0, 'Defense(Uruk-hai)':0, 'Dwarves':0, 'Elves':0, 'Ents':0,
                       'EquipmentType':'', 'Evil Men':0, 'HP(ALL)':0, 'HP(Beasts)':0, 'HP(Dwarves)':0,
                       'HP(Elves)':0, 'HP(Evil Men)':0, 'HP(Hobbits)':0, 'HP(Large Units)':0,
                       'HP(Melee)':0, 'HP(Men)':0, 'HP(Mounted Units)':0, 'HP(Orcs)':0, 'HP(Ranged)':0,
                       'HP(Trolls)':0, 'HP(Undead)':0, 'HP(Uruk-Hai)':0, 'HP(Uruk-hai)':0, 'Hobbits':0,
                       'Maiar':0, 'Men':0, 'Orcs':0, 'Perks':0,  'RequiredRaces':0,
                       'Siege(ALL)':0, 'Siege(Beasts)':0, 'Siege(Dwarves)':0, 'Siege(Elves)':0,
                       'Siege(Evil Men)':0, 'Siege(Hobbits)':0, 'Siege(Large Units)':0,
                       'Siege(Melee)':0, 'Siege(Men)':0, 'Siege(Mounted Units)':0, 'Siege(Orcs)':0,
                       'Siege(Ranged)':0, 'Siege(Trolls)':0, 'Siege(Undead)':0, 'Siege(Uruk-Hai)':0,
                       'Siege(Uruk-hai)':0, 'Speed(ALL)':0, 'Speed(Beasts)':0, 'Speed(Dwarves)':0,
                       'Speed(Elves)':0, 'Speed(Evil Men)':0, 'Speed(Hobbits)':0,
                       'Speed(Large Units)':0, 'Speed(Melee)':0, 'Speed(Men)':0,
                       'Speed(Mounted Units)':0, 'Speed(Orcs)':0, 'Speed(Ranged)':0, 'Speed(Trolls)':0,
                       'Speed(Undead)':0, 'Speed(Uruk-Hai)':0, 'Speed(Uruk-hai)':0, 'Undead':0,
                       'Uruk-hai':0}
        self.equipment_df=pd.DataFrame([blank_equips])
    def sum_equipment_stats(self):
        self.reset_equipment_df()
        weapon_df=self.weapon.get_stats()
        chest_df=self.chest.get_stats()
        head_df=self.head.get_stats()
        accessory_df=self.accessory.get_stats()
        
        if(len(weapon_df)>0):
            self.equipment_df=weapon_df
        if(len(chest_df)>0):
                self.equipment_df+=chest_df
        if(len(head_df)>0):
                self.equipment_df+=head_df
                
        if(len(accessory_df)>0):
                self.equipment_df+=accessory_df

        self.equipment_df=self.equipment_df.iloc[0]
        self.equipChanged.emit()
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
        self.sum_equipment_stats()
        Might+=self.equipment_df["CommanderMight"]
        Focus+=self.equipment_df["CommanderFocus"]
        Speed+=self.equipment_df["CommanderSpeed"]
        self.Might=Might
        self.Focus=Focus
        self.Speed=Speed
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


