'''
Created on Aug 14, 2022

@author: Billy Culver
'''



class BaseUnit():
    def __init__(self,unit):
        self.base_attack=unit.attack_stat.current_value()
        self.base_defense=unit.attack_stat.current_value()
        self.base_speed=unit.attack_stat.current_value()
        self.base_hp=unit.attack_stat.current_value()