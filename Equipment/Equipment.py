'''
Created on Jun 20, 2022

@author: Billy Culver
'''
from PySide2.QtWidgets import QWidget, QComboBox, QGridLayout, QLabel, QSpinBox

class EquipmentBase(QWidget):

    def __init__(self,df):
        QWidget.__init__(self)
        self.full_df=df
        self.itemSelect=QComboBox()
        
        self.refinement_label=QLabel("Refinement")
        self.strengthen_label=QLabel("Strengthen")
        self.strengthenSelect=QSpinBox()
        self.refinementSelect=QSpinBox()
        self.strengthenSelect.setMinimum(0)
        self.refinementSelect.setMinimum(0)
        
        
        self.itemSelect.currentIndexChanged.connect(self.update_item)
        
        
        
        l=QGridLayout()
        l.addWidget(self.itemSelect,0,0,1,-1)
        l.addWidget(self.strengthen_label,1,0)
        l.addWidget(self.strengthenSelect,1,1)
        l.addWidget(self.refinement_label,1,2)
        l.addWidget(self.refinementSelect,1,3)
        self.setLayout(l)
        
    def update_item(self):
        
        self.selected_Item=self.partial_df.loc[self.itemSelect.currentText()]
        if(self.selected_Item["Rarity"]==1):
            self.strengthenSelect.setMaximum(0)
        elif(self.selected_Item["Rarity"]==2):
            self.strengthenSelect.setMaximum(4)
        else:
            self.strengthenSelect.setMaximum(5)
        
        self.refinementSelect.setMaximum(self.strengthenSelect.value())
    def set_commander_restrictions(self,race):
        if(race=="IGNORE"):
            self.partial_df=self.full_df
        else:
            self.partial_df=self.full_df[self.full_df[race].astype(bool)]
        # print(self.partial_df)
        
        self.itemSelect.clear()
        self.itemSelect.addItems(self.partial_df.index.sort_values())