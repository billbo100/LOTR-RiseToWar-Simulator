'''
Created on Jun 22, 2022

@author: Billy Culver
'''
from PySide6.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel, QSpinBox,\
    QSlider
import pandas as pd
from PySide6.QtCore import Qt, Signal
from Calculations.UnitDamage import CalcUnitDamage
class UnitBase(QWidget):
    dmg_changed=Signal()
    def __init__(self):
        QWidget.__init__(self)
        self.empty_stats()
        self.load_Unit_List()
        self.label=QLabel("Units")
        self.UnitSelect=QComboBox()
        self.update_Unit_select()
        self.UnitCount=QSlider(Qt.Horizontal)
        self.UnitCount.setMinimum(0)
        self.UnitCount.setMaximum(0)
        self.UnitCountLabel=QLabel('0')
        self.attack_stat=QLabel("Attack: N/A")
        self.defense_stat=QLabel("Defense: N/A")
        self.HP_stat=QLabel("HP: N/A")
        self.speed_stat=QLabel("Speed: N/A")
        self.currentCommands=0
        self.UnitSelect.currentIndexChanged.connect(self.update_Unit_Stats)
        self.UnitCount.valueChanged.connect(self.calculate_commands)
        self.UnitCount.valueChanged.connect(self.update_count_label)
        self.UnitCount.valueChanged.connect(self.update_dmg)
        self.UnitCount.valueChanged.connect(self.update_total_health)
        
        self.dmg_estimate=QLabel("Damage Estimate:")
        
        
        self.min_estimate=0
        self.max_estimate=0
        
        self.buffs=[]
        self.debuffs=[]
        self.enemy_defense=0
        
        l=QGridLayout()
        l.addWidget(self.label,0,0,1,1)
        l.addWidget(self.UnitSelect,1,0,1,2)
        l.addWidget(self.UnitCount,2,0,1,1)
        l.addWidget(self.UnitCountLabel,2,1,1,1)
        l.addWidget(self.attack_stat,3,0,1,2)
        l.addWidget(self.defense_stat,4,0,1,2)
        l.addWidget(self.HP_stat,5,0,1,2)
        l.addWidget(self.speed_stat,6,0,1,2)
        l.addWidget(self.dmg_estimate,7,0,1,2)
        self.setLayout(l)
    def empty_stats(self):
        
        blank_equip={'Name':'','Rarity':0,'EquipmentType':0,'CommanderMight':0,'CommanderFocus':0,
                     'CommanderSpeed':0,'Dwarves':0,'Elves':0,'Ents':0,'Evil Men':0,'Hobbits':0,'Maiar':0,
                     'Men':0,'Orcs':0,'Undead':0,'Uruk-hai':0,'Attack(ALL)':0,'Attack(Beasts)':0,
                     'Attack(Dwarves)':0,'Attack(Elves)':0,'Attack(Evil Men)':0,'Attack(Melee)':0,
                     'Attack(Men)':0,'Attack(Orcs)':0,'Attack(Ranged)':0,'Attack(Trolls)':0,
                     'Attack(Undead)':0,'Attack(Uruk-hai)':0,'Defense(ALL)':0,'Defense(Beasts)':0,
                     'Defense(Dwarves)':0,'Defense(Elves)':0,'Defense(Evil Men)':0,
                     'Defense(Large Units)':0,'Defense(Melee)':0,'Defense(Men)':0,
                     'Defense(Mounted Units)':0,'Defense(Orcs)':0,'Defense(Ranged)':0,
                     'Defense(Trolls)':0,'Defense(Uruk-hai)':0,'HP(ALL)':0,'HP(Dwarves)':0,
                     'HP(Elves)':0,'HP(Evil Men)':0,'HP(Hobbits)':0,'HP(Melee)':0,'HP(Men)':0,
                     'HP(Orcs)':0,'HP(Ranged)':0,'HP(Undead)':0,'HP(Uruk-hai)':0,'Siege(Uruk-hai)':0,
                     'Speed(ALL)':0,'Speed(Beasts)':0,'Speed(Elves)':0,'Speed(Evil Men)':0,
                     'Speed(Melee)':0,'Speed(Men)':0,'Speed(Mounted Units)':0,'Speed(Orcs)':0,
                     'Speed(Ranged)':0,'Speed(Trolls)':0,'Speed(Uruk-Hai)':0,'Perks':''}
        self.equipment_stats=pd.Series(blank_equip)
    def updateEquipment(self,equip_series):
        self.equipment_stats=equip_series
        self.update_Unit_Stats()
    def get_equip_stats(self):
        damage=0
        defense=0
        hp=0
        speed=0
        siege=0
        current_unit=self.Unit_DF.loc[self.UnitSelect.currentText()]
        #add any values that include ALL
        damage+=self.equipment_stats["Attack(ALL)"]
        defense+=self.equipment_stats["Defense(ALL)"]
        hp+=self.equipment_stats["HP(ALL)"]
        speed+=self.equipment_stats["Speed(ALL)"]
        siege+=self.equipment_stats["Siege(ALL)"]
        
        #add any for their race
        damage+=self.equipment_stats["Attack(%s)"%current_unit["Race"]]
        defense+=self.equipment_stats["Defense(%s)"%current_unit["Race"]]
        hp+=self.equipment_stats["HP(%s)"%current_unit["Race"]]
        speed+=self.equipment_stats["Speed(%s)"%current_unit["Race"]]
        siege+=self.equipment_stats["Siege(%s)"%current_unit["Race"]]
    
        #add any for their attackType
        damage+=self.equipment_stats["Attack(%s)"%current_unit["AttackType"]]
        defense+=self.equipment_stats["Defense(%s)"%current_unit["AttackType"]]
        hp+=self.equipment_stats["HP(%s)"%current_unit["AttackType"]]
        speed+=self.equipment_stats["Speed(%s)"%current_unit["AttackType"]]
        siege+=self.equipment_stats["Siege(%s)"%current_unit["AttackType"]]
        #add any for being mounted
        if("Mounted" in current_unit["UnitType"]):
            damage+=self.equipment_stats["Attack(Mounted Units)"]
            defense+=self.equipment_stats["Defense(Mounted Units)"]
            hp+=self.equipment_stats["HP(Mounted Units)"]
            speed+=self.equipment_stats["Speed(Mounted Units)"]
            siege+=self.equipment_stats["Siege(Mounted Units)"]
        if("Large" in current_unit["UnitType"]):
            damage+=self.equipment_stats["Attack(Large Units)"]
            defense+=self.equipment_stats["Defense(Large Units)"]
            hp+=self.equipment_stats["HP(Large Units)"]
            speed+=self.equipment_stats["Speed(Large Units)"]
            siege+=self.equipment_stats["Siege(Large Units)"]
        self.equip_damage=damage
        self.equip_defense=defense
        self.equip_hp=hp
        self.equip_speed=speed
        self.equip_siege=siege
    def update_count_label(self):
        current_unit=self.Unit_DF.loc[self.UnitSelect.currentText()]
        self.UnitCountLabel.setText(str(self.UnitCount.value()*current_unit["UnitsPerCommand"]))
    def calculate_commands(self):
        current_unit=self.Unit_DF.loc[self.UnitSelect.currentText()]
        self.currentCommands=self.UnitCount.value()
    def load_Unit_List(self):
        self.Unit_DF=pd.read_csv('data/Units.csv',index_col="Name")
    def setMaxCommand(self,c):
        self.maxCommands=c
        self.setMaxTroops()
    def setMaxTroops(self):
        if(self.UnitSelect.currentText()!="None"):
            self.UnitCount.setMaximum(self.maxCommands)
    def update_Unit_select(self):
        self.UnitSelect.addItems(["None"]+list(self.Unit_DF.index))
        
        
    def update_Unit_Stats(self):
        if(self.UnitSelect.currentText()=="None"):
            self.UnitCount.setMaximum(0)
            self.dmg_estimate.setText("Damage Estimate:")
            self.attack_stat.setText("Attack: N/A")
            self.defense_stat.setText("Defense: N/A")
            self.HP_stat.setText("HP: N/A")
            self.speed_stat.setText("Speed: N/A")
        else:
            current_unit=self.Unit_DF.loc[self.UnitSelect.currentText()]
            
            self.get_equip_stats()
            self.setMaxTroops()
            self.UnitCount.setValue(self.currentCommands*current_unit["UnitsPerCommand"])
            self.calculate_commands()
            self.attack_stat.setText("Attack: %d-%d"%(current_unit["MinDmg"]+self.equip_damage,current_unit["MaxDmg"]+self.equip_damage))
            self.defense_stat.setText("Defense: %d"%(current_unit["Defense"]+self.equip_defense))
            self.HP_stat.setText("HP: %d"%(current_unit["HP"]+self.equip_hp))
            self.speed_stat.setText("Speed: %d"%(current_unit["Speed"]+self.equip_speed))
            self.update_dmg()
            
            
    def set_buff_debuff_defense(self,defense,buffs,debuffs):
        print(buffs)
        self.buffs=[float(b) for b in buffs.split(',')]
        self.debuffs=[float(d) for d in debuffs.split(',')]
        self.enemy_defense=defense
        self.update_dmg()
    def update_dmg(self):  
        current_unit=self.Unit_DF.loc[self.UnitSelect.currentText()]      
        self.min_estimate=CalcUnitDamage(UnitCount=self.UnitCount.value()*current_unit["UnitsPerCommand"],
                           UnitsPerCommand=current_unit["UnitsPerCommand"],
                            minAttack=current_unit["MinDmg"]+self.equip_damage, 
                            MaxAttack=current_unit["MaxDmg"]+self.equip_damage, 
                            Buffs=self.buffs, 
                            Debuffs=self.debuffs, 
                            EnemyDefense=self.enemy_defense, 
                            damageType="Physical",
                            AttackRollType="Min")
        self.max_estimate=CalcUnitDamage(UnitCount=self.UnitCount.value()*current_unit["UnitsPerCommand"],
                           UnitsPerCommand=current_unit["UnitsPerCommand"],
                            minAttack=current_unit["MinDmg"]+self.equip_damage, 
                            MaxAttack=current_unit["MaxDmg"]+self.equip_damage, 
                            Buffs=self.buffs, 
                            Debuffs=self.debuffs, 
                            EnemyDefense=self.enemy_defense, 
                            damageType="Physical",
                            AttackRollType="Max")
        
        
        
        self.dmg_estimate.setText("Damage Estimate: %d-%d"%(self.min_estimate,self.max_estimate))
        self.dmg_changed.emit()
        
        
        
        
        
        
        
        
        
        
        
        
        
        