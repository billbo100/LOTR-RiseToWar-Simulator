from PySide6.QtWidgets import QWidget, QComboBox, QGridLayout
from Equipment.Equipment import EquipmentBase
import pandas as pd
from PySide6.QtCore import Signal
import os
import sys



class EquipmentSelect(QWidget):
    equipChanged=Signal()
    def __init__(self):
        QWidget.__init__(self)
        self.load_Equipment()
        self.Equipment_sort=QComboBox()
        all_vals=list(self.full_Equipment_DF.columns)
        non_sortable=["EquipmentType","Maiar","Men","Elves","Dwarves","Undead","Evil Men","Ents","Orcs","Uruk-hai","Hobbits","Chest","Perks"]
        sortable_vals=[x for x in all_vals if (not x in non_sortable)]
        self.Equipment_sort.addItems(sortable_vals)
        self.Equipment_sort.currentIndexChanged.connect(self.set_update_equipment_sorting)
        # print(self.full_Equipment_DF[self.full_Equipment_DF["EquipmentType"]=="Weapon"])
        # print(self.perk_DF)
        
        self.weapon=EquipmentBase(self.full_Equipment_DF[self.full_Equipment_DF["EquipmentType"]=="Weapon"],self.perk_DF)
        
        self.weapon.itemSelect.currentIndexChanged.connect(self.change_equip)
        self.weapon.strengthenSelect.valueChanged.connect(self.change_equip)
        self.weapon.refinementSelect.valueChanged.connect(self.change_equip)
        
        self.chest=EquipmentBase(self.full_Equipment_DF[self.full_Equipment_DF["EquipmentType"]=="Armor"],self.perk_DF)
        self.chest.itemSelect.currentIndexChanged.connect(self.change_equip)
        self.chest.strengthenSelect.valueChanged.connect(self.change_equip)
        self.chest.refinementSelect.valueChanged.connect(self.change_equip)
        self.head=EquipmentBase(self.full_Equipment_DF[self.full_Equipment_DF["EquipmentType"]=="Helmet"],self.perk_DF)
        self.head.itemSelect.currentIndexChanged.connect(self.change_equip)
        self.head.strengthenSelect.valueChanged.connect(self.change_equip)
        self.head.refinementSelect.valueChanged.connect(self.change_equip)
        
        self.accessory=EquipmentBase(self.full_Equipment_DF[self.full_Equipment_DF["EquipmentType"]=="Accessory"],self.perk_DF)
        self.accessory.itemSelect.currentIndexChanged.connect(self.change_equip)
        self.accessory.strengthenSelect.valueChanged.connect(self.change_equip)
        self.accessory.refinementSelect.valueChanged.connect(self.change_equip)
        l=QGridLayout()
        l.addWidget(self.Equipment_sort,1,3)
        l.addWidget(self.weapon,2,0)
        l.addWidget(self.chest,2,1)
        l.addWidget(self.head,2,2)
        l.addWidget(self.accessory,2,3)
        self.setLayout(l)
    def change_equip(self):
        self.equipChanged.emit()
    def load_Equipment(self):
        self.full_Equipment_DF=pd.read_csv("data/EquipmentFull.csv",index_col="Name")
        self.perk_DF=pd.read_csv("data/EquipPerkProccessed.csv",index_col="Name")
    def set_update_equipment_sorting(self):
        self.weapon.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
        self.chest.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
        self.head.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
        self.accessory.set_commander_restrictions(self.Commander['Race'],self.Equipment_sort.currentText())
    def sum_equipment_stats(self):
        try:
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
        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
    def reset_equipment_df(self):
        blank_equips={ 'Rarity':0,'CommanderMight':0,'CommanderFocus':0, 'CommanderSpeed':0,'Attack(ALL)':0, 
                       'Attack(Beasts)':0, 'Attack(Dwarves)':0, 'Attack(Elves)':0,
                       'Attack(Evil Men)':0, 'Attack(Hobbits)':0, 'Attack(Large Units)':0,
                       'Attack(Melee)':0, 'Attack(Men)':0, 'Attack(Mounted Units)':0, 'Attack(Orcs)':0,
                       'Attack(Ranged)':0, 'Attack(Trolls)':0, 'Attack(Undead)':0,
                       'Attack(Uruk-Hai)':0, 'Chest':'', 'Defense(ALL)':0, 'Defense(Beasts)':0,
                       'Defense(Dwarves)':0, 'Defense(Elves)':0, 'Defense(Evil Men)':0,
                       'Defense(Hobbits)':0, 'Defense(Large Units)':0, 'Defense(Melee)':0,
                       'Defense(Men)':0, 'Defense(Mounted Units)':0, 'Defense(Orcs)':0,
                       'Defense(Ranged)':0, 'Defense(Trolls)':0, 'Defense(Undead)':0,
                       'Defense(Uruk-Hai)':0, 'Dwarves':0, 'Elves':0, 'Ents':0,
                       'EquipmentType':'', 'Evil Men':0, 'HP(ALL)':0, 'HP(Beasts)':0, 'HP(Dwarves)':0,
                       'HP(Elves)':0, 'HP(Evil Men)':0, 'HP(Hobbits)':0, 'HP(Large Units)':0,
                       'HP(Melee)':0, 'HP(Men)':0, 'HP(Mounted Units)':0, 'HP(Orcs)':0, 'HP(Ranged)':0,
                       'HP(Trolls)':0, 'HP(Undead)':0, 'HP(Uruk-Hai)':0, 'Hobbits':0,
                       'Maiar':0, 'Men':0, 'Orcs':0, 'Perks':'',  'RequiredRaces':'',
                       'Siege(ALL)':0, 'Siege(Beasts)':0, 'Siege(Dwarves)':0, 'Siege(Elves)':0,
                       'Siege(Evil Men)':0, 'Siege(Hobbits)':0, 'Siege(Large Units)':0,
                       'Siege(Melee)':0, 'Siege(Men)':0, 'Siege(Mounted Units)':0, 'Siege(Orcs)':0,
                       'Siege(Ranged)':0, 'Siege(Trolls)':0, 'Siege(Undead)':0, 'Siege(Uruk-Hai)':0,
                       'Speed(ALL)':0, 'Speed(Beasts)':0, 'Speed(Dwarves)':0,
                       'Speed(Elves)':0, 'Speed(Evil Men)':0, 'Speed(Hobbits)':0,
                       'Speed(Large Units)':0, 'Speed(Melee)':0, 'Speed(Men)':0,
                       'Speed(Mounted Units)':0, 'Speed(Orcs)':0, 'Speed(Ranged)':0, 'Speed(Trolls)':0,
                       'Speed(Undead)':0, 'Speed(Uruk-Hai)':0, 'Undead':0,
                       'Uruk-Hai':0}
        self.equipment_df=pd.DataFrame([blank_equips])    
        
        
        
        
        
        
        