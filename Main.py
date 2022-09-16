from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget,\
    QPushButton
from PySide6.QtCore import Qt
import sys
from GUI.ArmyClass import Army
from PySide6.QtGui import QFont
import os
import logging
from simulation_thread import simulation_thread
class BattleSim(QMainWindow):
    def __init__(self):
        try:
            
            QMainWindow.__init__(self)
            self.mainWidget=QWidget()
            self.font=QFont("Arial",12)
            
            self.sim_thread=simulation_thread()
            
            self.setFont(self.font)
            self.setCentralWidget(self.mainWidget)
            
            self.Attacker=Army("Attacking Army")
            self.Defender=Army("Defending Army")
            
            self.run_sim_btn=QPushButton("Run Sim")
            self.run_sim_btn.clicked.connect(self.run_simulation)
            
            l=QGridLayout()
            l.addWidget(self.Attacker,0,0)
            l.addWidget(self.Defender,0,1)
            self.mainWidget.setLayout(l)
        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
            logging.error('%s:%s in %s at %d'%(exc_type.__name__,str(e), fname, exc_tb.tb_lineno))
        
    def run_simulation(self):
        self.sim_thread.set_armies(self.Attacker,self.Defender)
        self.sim_thread.run()

if __name__ == '__main__':
    # Handle high resolution displays:
    QApplication.setAttribute(Qt.AA_Use96Dpi)
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_Use96Dpi)
    # app.setStyle("Fusion")
    aw = BattleSim()
    aw.show()
    app.exec()   
