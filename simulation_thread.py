from PySide6.QtCore import QThread


class simulation_thread(QThread):
    def __init__(self):
        QThread.__init__(self)
    def set_armies(self,attacker,defender):
        self.a_army=attacker
        self.d_army=defender
    def run(self):
        #run best case scenario
        #run worst case scenario
        #run 1000 random scenarios
        
        run_simulation(self.a_army,self.d_army,type="Random")
        
        
        
        
        
        
        
        
def run_simulation(attacker,defender,type="Random"):
    au1=attacker.units.Unit1
    au2=attacker.units.Unit2
    au3=attacker.units.Unit3
    du1=defender.units.Unit1
    du2=defender.units.Unit2
    du3=defender.units.Unit3
    ac=attacker.commander
    dc=defender.commander