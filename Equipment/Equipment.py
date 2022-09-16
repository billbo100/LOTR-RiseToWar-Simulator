'''
Created on Jun 20, 2022

@author: Billy Culver
'''
from PySide6.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel, QSpinBox
from math import floor
from PySide6.QtGui import QColor, QFont
import numpy as np
from fractions import Fraction
from string import Template
from textwrap import TextWrapper
import pandas as pd
class EquipmentBase(QWidget):
    def __init__(self,equip_df,perk_df):
        
        QWidget.__init__(self)
        self.full_df=equip_df
        
        self.perk_df=perk_df
        
        self.itemSelect=QComboBox()
        self.itemSelect.setStyleSheet('selection-background-color: rgba(0,0,0,0)')
        self.itemSelect.setStyleSheet('QComboBox{selection-border-color: rgb(0,0,0);}')
        self.itemSelect.setFont(QFont("Arial",16)) 
        self.selected_Item=[]
        
        self.refinement_label=QLabel("Refinement")
        self.strengthen_label=QLabel("Strengthen")
        self.strengthenSelect=QSpinBox()
        self.refinementSelect=QSpinBox()
        self.strengthenSelect.setMinimum(0)
        self.refinementSelect.setMinimum(0)
        self.perk=QLabel()
        self.perkSelect=QComboBox()
        self.perkSelect.currentIndexChanged.connect(self.update_perk)
        self.level_chart=[1,1.3,1.6,2,2.5,3]
        self.itemSelect.currentIndexChanged.connect(self.update_item)
        self.strengthenSelect.valueChanged.connect(self.update_strengthen)
        self.wrapper=TextWrapper(35)
        self.refinementSelect.valueChanged.connect(self.update_perk)
        l=QGridLayout()
        l.addWidget(self.itemSelect,0,0,1,-1)
        l.addWidget(self.strengthen_label,1,0)
        l.addWidget(self.strengthenSelect,1,1)
        l.addWidget(self.refinement_label,2,0)
        l.addWidget(self.refinementSelect,2,1)
        l.addWidget(self.perkSelect,3,0,1,-1)
        l.addWidget(self.perk,4,0,1,-1)
        self.setLayout(l)
    def update_strengthen(self):
        if(len(self.selected_Item)>0):
            if(self.selected_Item["Rarity"]>2):
                self.refinementSelect.setMaximum(self.strengthenSelect.value())
    def update_perk(self):
        
        self.perk.setText('')
        name=self.perkSelect.currentText()
        if(name!=''):
            perk=self.perk_df.loc[name]
            eff=perk["Effect"]
            if("$VAL") in eff:
                start_vs=[float(Fraction(sv)) for sv in np.array(str(perk["StartVal"]).split("|"))]
                
                per_vals=np.array([float(Fraction(pv)) for pv in perk["PerRefinement"].split("|")])*self.refinementSelect.value()
                vals=np.round(start_vs+per_vals,1)
                t=Template(eff)
                effect_descript=t.substitute(VAL=vals[0])
                self.perk.setText(self.wrapper.fill("%s:%s"%(name,effect_descript)))
                
                
    def update_item(self):
        self.perkSelect.clear()
        if(self.itemSelect.currentText()!='' and self.itemSelect.currentIndex()!=0):
            self.selected_Item=self.partial_df.loc[self.itemSelect.currentText().split('(')[0].strip()]
            if(self.selected_Item["Perks"]!="0"):
                self.perkSelect.addItems(self.selected_Item["Perks"].split("|"))
                self.update_perk()
                if(self.selected_Item["Rarity"]==1):
                    self.strengthenSelect.setMaximum(0)
                    self.refinementSelect.setMaximum(0)
                elif(self.selected_Item["Rarity"]==2):
                    self.strengthenSelect.setMaximum(4)
                    self.refinementSelect.setMaximum(0)
                elif(self.selected_Item["Rarity"]==3):
                    self.strengthenSelect.setMaximum(5)
                    self.refinementSelect.setMaximum(self.strengthenSelect.value())
                else:
                    self.strengthenSelect.setMaximum(5)
                    self.refinementSelect.setMaximum(self.strengthenSelect.value())
        else:
            self.selected_Item=[]
            self.strengthenSelect.setMaximum(0)
            self.refinementSelect.setMaximum(0)     
            
    def set_commander_restrictions(self,race,sort_val):
        if(race=="IGNORE"):
            self.partial_df=self.full_df
        else:
            self.partial_df=self.full_df[self.full_df[race].astype(bool)]
        self.update_Equipment_Combobox(sort_val)
    def update_Equipment_Combobox(self,sort_val):
        current_item=self.itemSelect.currentText().split('(')[0].strip()
        self.itemSelect.clear()
        vals=[]
        if("(" in sort_val) and (not "ALL" in sort_val) : 
            sort_parts=sort_val.split('(')
            st=sort_parts[0].strip()
            st_ALL=st+"(ALL)"
            self.partial_df.insert(len(self.partial_df.keys()),"SUM",self.partial_df[st_ALL]+self.partial_df[sort_val])
            vals=self.partial_df.sort_values(["SUM","Rarity","Name"],ascending=[False,False,True])
            vals=["%s (%s)"%(i,v["SUM"]) for i,v in vals.iterrows()]
          
        else:
            vals=self.partial_df.sort_values([sort_val,"Rarity","Name"],ascending=[False,False,True])
            vals=["%s (%s)"%(i,v[sort_val]) for i,v in vals.iterrows()]
        self.itemSelect.addItems(["None"]+vals)
        found=False
        for i in range(self.itemSelect.count()):
            if(i!=0):
                
                item=self.full_df.loc[self.itemSelect.itemText(i).split('(')[0].strip()]
                if(current_item in item.name and current_item!=''):
                    self.itemSelect.setCurrentIndex(i)
                    found=True
                if(item["Rarity"]==1):
                    color=QColor(144,238,144)
                elif(item["Rarity"]==2):
                    color=QColor(144,144,255)
                elif(item["Rarity"]==3):
                    color=QColor(174, 50, 160)
                elif(item["Rarity"]==4):
                    color=QColor(255,255,144)
            else:
                color=QColor(255,255,255)
            self.itemSelect.model().item(i).setBackground(color)
        if(not found):
            self.itemSelect.setCurrentIndex(0)
        
    def get_stats(self):
        if(len(self.selected_Item)>0):
            temp_df=pd.DataFrame([self.selected_Item.to_dict()])
            invalid_columns=['Dwarves','Elves', 'Ents', 'Evil Men', 'Hobbits', 'Maiar', 'Men', 'Orcs',
                             'Undead', 'Uruk-hai','Perks','Rarity','EquipmentType','Name']
            temp_df.iloc[0,~np.in1d(temp_df.columns,invalid_columns)]=temp_df.iloc[0,~np.in1d(temp_df.columns,invalid_columns)]
            temp_df.at[0,"Perks"]=self.perkSelect.currentText()+'|'
            cols = temp_df.select_dtypes(np.number).columns
            temp_df[cols] = temp_df[cols].mul(self.level_chart[self.strengthenSelect.value()])
            return temp_df
        else:
            return pd.DataFrame([])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        