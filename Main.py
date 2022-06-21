from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout,\
    QLabel
from PySide2.QtCore import Qt
import sys
from GUI.ArmyClass import Army
import pandas as pd
class BattleSim(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.mainWidget=QWidget()
        
        self.setCentralWidget(self.mainWidget)
        
        self.Attacker=Army("Attacking Army")
        self.Defender=Army("Defending Army")
        
        
        
        l=QGridLayout()
        l.addWidget(self.Attacker,0,0)
        # l.addWidget(self.Defender,0,1)
        self.mainWidget.setLayout(l)

    








if __name__ == '__main__':
    # Handle high resolution displays:
    QApplication.setAttribute(Qt.AA_Use96Dpi)
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_Use96Dpi)
    # app.setStyle("Fusion")
    aw = BattleSim()
    aw.show()
    app.exec_()   