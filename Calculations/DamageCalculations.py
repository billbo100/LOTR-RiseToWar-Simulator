'''
Created on Jun 17, 2022

@author: Billy Culver
'''
import numpy as np
def Defense_reduction(Defense):
    return (0.9*Defense)/(Defense+120)
def CommanderNormalCommandCount(CommandCount):
    return (25*CommandCount)/(CommandCount+75)+4
def CommanderSkillCommandCount(CommandCount):
    return(25*CommandCount)/(CommandCount+75)+2


def CommanderDamagePhysical(DamageMultiplier,might,buff_list,debuff_list,Defense,CommandCount,isNormal):
    if(isNormal):
        comm_factor=CommanderNormalCommandCount(CommandCount)
    else:
        comm_factor=CommanderSkillCommandCount(CommandCount)
        
    buff_debuff_defense=max(0.1,(1+np.sum(buff_list+debuff_list)-Defense_reduction(Defense)))
    return DamageMultiplier*might*buff_debuff_defense*comm_factor


def CommanderDamageElemental(DamageMultiplier,Focus,buff_list,debuff_list,CommandCount,isNormal):
    comm_factor=CommanderSkillCommandCount(CommandCount)
    Buff_debuff=max(0.1,(1+np.sum(buff_list+debuff_list)))
    
    return Buff_debuff*(2*Focus+DamageMultiplier*100*comm_factor)
    
    
if __name__ == '__main__':
    print(CommanderDamageElemental(DamageMultiplier=2, Focus=400, buff_list=[0.5], debuff_list=[-0.08], CommandCount=75, isNormal=True))