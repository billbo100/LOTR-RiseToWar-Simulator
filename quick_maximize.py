'''
Created on Aug 11, 2022

@author: Billy Culver
'''
from scipy.optimize import minimize
from Calculations.UnitDamage import CalcUnitDamage
import numpy as np
import matplotlib.pyplot as plt
def troop_count_con(xyz):
    x=xyz[0]
    y=xyz[1]
    z=xyz[2]
    return x+y+z-75

def total_damage(troop_counts,t1_boost,t2_boost,t3_boost,enemy_defense,full_troop_damage_boost,enemy_damage_reduction,t1_tpc,t2_tpc,t3_tpc,t1_min,t2_min,t3_min,t1_max,t2_max,t3_max):
    t1_damage=CalcUnitDamage(troop_counts[0]*t1_tpc, t1_tpc, minAttack=t1_min, MaxAttack=t1_max, Buffs=[t1_boost+full_troop_damage_boost], Debuffs=[enemy_damage_reduction], EnemyDefense=enemy_defense, damageType="Physical", AttackRollType='Average')
    t2_damage=CalcUnitDamage(troop_counts[1]*t2_tpc, t2_tpc, minAttack=t2_min, MaxAttack=t2_max, Buffs=[t2_boost+full_troop_damage_boost], Debuffs=[enemy_damage_reduction], EnemyDefense=enemy_defense, damageType="Physical", AttackRollType='Average')
    t3_damage=CalcUnitDamage(troop_counts[2]*t3_tpc, t3_tpc, minAttack=t3_min, MaxAttack=t3_max, Buffs=[t3_boost+full_troop_damage_boost], Debuffs=[enemy_damage_reduction], EnemyDefense=enemy_defense, damageType="Physical", AttackRollType='Average')
    
    
    # print("T1:",troop_counts[0],t1_damage)
    # print("T2:",troop_counts[1],t2_damage)
    # print("T3:",troop_counts[2],t3_damage)
    # print("DAMAGE:",t1_damage+t2_damage+t3_damage)
    # print()
    
    return -(t1_damage+t2_damage+t3_damage)
if __name__ == '__main__':
    
    
    enemy_defense=0
    enemy_damage_reduction=0.0
    full_troop_damage_boost=0.
    t1_boost=0
    t2_boost=0.4
    t3_boost=0.2
    
    t1_tpc=100
    t2_tpc=100
    t3_tpc=100
    
    t1_min=28
    t1_max=29
    
    t2_min=18
    t2_max=26
    
    t3_min=9
    t3_max=29
    
    
    
    def_ranges= range(0,150,1)
    t1s=[]
    t2s=[]
    t3s=[]
    
    
    
    for enemy_defense in def_ranges:
        const_args=(t1_boost,t2_boost,t3_boost, enemy_defense,full_troop_damage_boost,enemy_damage_reduction,t1_tpc,t2_tpc,t3_tpc,t1_min,t2_min,t3_min,t1_max,t2_max,t3_max)
        min_results=minimize(total_damage,x0=[25,25,25],args=const_args,constraints = {'type':'eq', 'fun': troop_count_con},bounds=[(0,75),(0,75),(0,75)])
        
        comm_counts=np.round(min_results.x)
        
        
        sm=np.sum(comm_counts)
        if(sm>75):
            comm_counts[np.argmax(comm_counts)]-=1
        elif(sm<75):
            comm_counts[np.argmin(comm_counts)]+=1
    
        sm=np.sum(np.round(comm_counts))
        print(comm_counts,sm)
        t1s.append(comm_counts[0])
        t2s.append(comm_counts[1])
        t3s.append(comm_counts[2])
    plt.plot(def_ranges,t1s,label='Sentinels')
    plt.plot(def_ranges,t2s,label='Sharpshooters')
    plt.plot(def_ranges,t3s,label='Master Throwers')
    plt.legend()
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    