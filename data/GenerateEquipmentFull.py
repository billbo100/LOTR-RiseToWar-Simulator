'''
Created on Jun 19, 2022

@author: Culver
'''
import pandas as pd
import numpy as np

df=pd.read_csv("Equipment.csv",dtype=str)
df.dropna(inplace=True,how="all")
print(df)
all_races=set()
all_bonuses=set()
for i,l in df.iterrows():
    if("?" in l["Name"]):
        continue
    races=l.RequiredRaces.split('|')
    all_races=all_races.union(set(races))
    for r in races:
        df.at[i,r]=1
    
    if(str(l.UnitBonuses)!='nan'):
        parts=[b.split('+') for b in l.UnitBonuses.split('|')]
        # print(parts)
        for p in parts:
            df.at[i,p[0]]=p[1]
            all_bonuses.add(p[0])

df.fillna(0,inplace=True)
all_races=list(all_races)
all_bonuses=list(all_bonuses)

all_races.sort()
print(all_races)

all_bonuses.sort()
print(all_bonuses)
columns=['Name','Rarity',"EquipmentType",'CommanderMight','CommanderFocus','CommanderSpeed']+all_races+all_bonuses+["Perks"]
df.to_csv("EquipmentFull.csv",columns=columns,index=False)