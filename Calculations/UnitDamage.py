'''
Created on Jun 22, 2022

@author: Billy Culver
'''
from Calculations.DamageCalculations import Defense_reduction
import numpy as np
def CalcUnitDamage(UnitCount,UnitsPerCommand,minAttack,MaxAttack,Buffs,Debuffs,EnemyDefense,damageType="Physical",AttackRollType="Random"):
    Commands=UnitCount/UnitsPerCommand
    EffectiveUnits=(50/ 3) * Commands / (75+Commands) * UnitsPerCommand
    
    
    if(damageType=="Physical"):
        buff_total=max(0.1,(1+np.sum(Buffs+Debuffs)-Defense_reduction(EnemyDefense)))
    else:
        buff_total=max(0.1,(1+np.sum(Buffs+Debuffs)))
    if(AttackRollType=="Random"):
        AttackRoll=minAttack+np.random.rand()*(MaxAttack-minAttack)
    elif(AttackRollType=="Average"):
        AttackRoll=(minAttack+MaxAttack)/2
    elif(AttackRollType=="Max"):
        AttackRoll=MaxAttack
    elif(AttackRollType=="Min"):
        AttackRoll=minAttack
        
        
    return buff_total*AttackRoll*EffectiveUnits
    
    
# d=CalcUnitDamage(UnitCount=2987, UnitsPerCommand=100, minAttack=19, MaxAttack=19, Buffs=[0.09,0.15,0.45,0.10], Debuffs=[-.08], EnemyDefense=31)
# print(d)