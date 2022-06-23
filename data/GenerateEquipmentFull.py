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

all_races.sort()
print(all_races)

all_bonus_types=set()
for v in all_bonuses:
    t=v.split('(')[1][:-1]
    if(not"Attack(%s)"%t in df.columns):
        df["Attack(%s)"%t]=0
    if(not"Defense(%s)"%t in df.columns):
        df["Defense(%s)"%t]=0
        print("Defense(%s)"%t)
    if(not"HP(%s)"%t in df.columns):
        df["HP(%s)"%t]=0
    if(not"Speed(%s)"%t in df.columns):
        df["Speed(%s)"%t]=0
    if(not"Siege(%s)"%t in df.columns):
        df["Siege(%s)"%t]=0
    all_bonus_types.add("Attack(%s)"%t)
    all_bonus_types.add("Defense(%s)"%t)
    all_bonus_types.add("HP(%s)"%t)
    all_bonus_types.add("Speed(%s)"%t)
    all_bonus_types.add("Siege(%s)"%t)
all_bonus_types=list(all_bonus_types)
all_bonus_types.sort()
print(df.columns.sort_values())
cols=[ 'Rarity','Name','CommanderMight','CommanderFocus', 'CommanderSpeed','Attack(ALL)', 
       'Attack(Beasts)', 'Attack(Dwarves)', 'Attack(Elves)',
       'Attack(Evil Men)', 'Attack(Hobbits)', 'Attack(Large Units)',
       'Attack(Melee)', 'Attack(Men)', 'Attack(Mounted Units)', 'Attack(Orcs)',
       'Attack(Ranged)', 'Attack(Trolls)', 'Attack(Undead)',
       'Attack(Uruk-Hai)', 'Attack(Uruk-hai)', 'Chest', 'Defense(ALL)', 'Defense(Beasts)',
       'Defense(Dwarves)', 'Defense(Elves)', 'Defense(Evil Men)',
       'Defense(Hobbits)', 'Defense(Large Units)', 'Defense(Melee)',
       'Defense(Men)', 'Defense(Mounted Units)', 'Defense(Orcs)',
       'Defense(Ranged)', 'Defense(Trolls)', 'Defense(Undead)',
       'Defense(Uruk-Hai)', 'Defense(Uruk-hai)', 'Dwarves', 'Elves', 'Ents',
       'EquipmentType', 'Evil Men', 'HP(ALL)', 'HP(Beasts)', 'HP(Dwarves)',
       'HP(Elves)', 'HP(Evil Men)', 'HP(Hobbits)', 'HP(Large Units)',
       'HP(Melee)', 'HP(Men)', 'HP(Mounted Units)', 'HP(Orcs)', 'HP(Ranged)',
       'HP(Trolls)', 'HP(Undead)', 'HP(Uruk-Hai)', 'HP(Uruk-hai)', 'Hobbits',
       'Maiar', 'Men', 'Orcs', 'Perks',  'RequiredRaces',
       'Siege(ALL)', 'Siege(Beasts)', 'Siege(Dwarves)', 'Siege(Elves)',
       'Siege(Evil Men)', 'Siege(Hobbits)', 'Siege(Large Units)',
       'Siege(Melee)', 'Siege(Men)', 'Siege(Mounted Units)', 'Siege(Orcs)',
       'Siege(Ranged)', 'Siege(Trolls)', 'Siege(Undead)', 'Siege(Uruk-Hai)',
       'Siege(Uruk-hai)', 'Speed(ALL)', 'Speed(Beasts)', 'Speed(Dwarves)',
       'Speed(Elves)', 'Speed(Evil Men)', 'Speed(Hobbits)',
       'Speed(Large Units)', 'Speed(Melee)', 'Speed(Men)',
       'Speed(Mounted Units)', 'Speed(Orcs)', 'Speed(Ranged)', 'Speed(Trolls)',
       'Speed(Undead)', 'Speed(Uruk-Hai)', 'Speed(Uruk-hai)', 'Undead',
       'Uruk-hai']
df.to_csv("EquipmentFull.csv",columns=cols,index=False)