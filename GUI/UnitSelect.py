'''
Created on Aug 9, 2022

@author: Billy Culver
'''
from PySide6.QtWidgets import QWidget, QGridLayout
from Unit.Unit import UnitBase

class UnitSelect(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.Unit1=UnitBase()
        self.Unit2=UnitBase()
        self.Unit3=UnitBase()
        
        l=QGridLayout()
        l.addWidget(self.Unit1,0,0,1,1)
        l.addWidget(self.Unit2,0,1,1,1)
        l.addWidget(self.Unit3,0,2,1,1)
        self.setLayout(l)