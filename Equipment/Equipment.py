'''
Created on Jun 20, 2022

@author: Billy Culver
'''
from PySide2.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel, QSpinBox
from math import floor
from PySide2.QtGui import QColor

class EquipmentBase(QWidget):

    def __init__(self,df):
        QWidget.__init__(self)
        self.full_df=df
        self.itemSelect=QComboBox()
        self.itemSelect.setStyleSheet('selection-background-color: rgba(0,0,0,0)')
        self.itemSelect.setStyleSheet('QComboBox{selection-border-color: rgb(0,0,0);}')
        self.selected_Item=[]
        self.refinement_label=QLabel("Refinement")
        self.strengthen_label=QLabel("Strengthen")
        self.strengthenSelect=QSpinBox()
        self.refinementSelect=QSpinBox()
        self.strengthenSelect.setMinimum(0)
        self.refinementSelect.setMinimum(0)
        
        self.level_chart=[1,1.3,1.6,2,2.5,3]
        self.itemSelect.currentIndexChanged.connect(self.update_item)
        self.strengthenSelect.valueChanged.connect(self.update_strengthen)
        
        
        l=QGridLayout()
        l.addWidget(self.itemSelect,0,0,1,-1)
        l.addWidget(self.strengthen_label,1,0)
        l.addWidget(self.strengthenSelect,1,1)
        l.addWidget(self.refinement_label,2,0)
        l.addWidget(self.refinementSelect,2,1)
        self.setLayout(l)
    def update_strengthen(self):
        if(len(self.selected_Item)>0):
            if(self.selected_Item["Rarity"]>2):
                self.refinementSelect.setMaximum(self.strengthenSelect.value())
    def update_item(self):
        if(self.itemSelect.currentText()!='' and self.itemSelect.currentIndex()!=0):
            self.selected_Item=self.partial_df.loc[self.itemSelect.currentText().split('(')[0].strip()]
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
            # print(self.CommanderSelect.model().item(i).background())
        if(not found):
            self.itemSelect.setCurrentIndex(0)
        
    def get_stats(self):
        if(len(self.selected_Item)>0):
            m=floor(self.selected_Item["CommanderMight"]*self.level_chart[self.strengthenSelect.value()])
            f=floor(self.selected_Item["CommanderFocus"]*self.level_chart[self.strengthenSelect.value()])
            s=floor(self.selected_Item["CommanderSpeed"]*self.level_chart[self.strengthenSelect.value()])
            
            return m,f,s
        else:
            return 0,0,0
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        