
import numpy as np
from Calculations.DamageCalculations import CommanderDamagePhysical, CommanderNormalCommandCount, CommanderSkillCommandCount, Defense_reduction
class Effect():
    def __init__(self):
        pass
    def __str__(self):
        return ''

    def activate(self,targets):
        pass
    def select_targets(targets):
        return targets
class Damage(Effect):
    def __init__(self,activation_chance,DamageMultiplier,ntargets):
        self.activation_chance=activation_chance
        self.DamageMultiplier=DamageMultiplier #The percent damage. 240% --> 2.4 etc.
        super().__init__()

class PhysicalDamage(Damage):
    def __init__(self,activation_chance,DamageMultiplier):
        
        super().__init__()

class CommanderPhysicalDamage(PhysicalDamage):
    def __init__(self, activation_chance, DamageMultiplier,isnormal):
        self.isNormal=isnormal
        super().__init__(activation_chance, DamageMultiplier)
        
    def calculate_Damage(self,DamageMultiplier,might,buff_list,debuff_list,Defense,CommandCount,isNormal):
        if(self.isNormal):
            comm_factor=CommanderNormalCommandCount(CommandCount)
        else:
            comm_factor=CommanderSkillCommandCount(CommandCount)
        
        buff_debuff_defense=max(0.1,(1+np.sum(buff_list+debuff_list)-Defense_reduction(Defense)))
        return DamageMultiplier*might*buff_debuff_defense*comm_factor

    def activate(self, targets):
        selected_targets=self.select_target(targets)
        return self.calculate_Damage