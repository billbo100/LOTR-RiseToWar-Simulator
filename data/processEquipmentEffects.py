'''
Created on Jun 21, 2022

@author: Billy Culver
'''

import pandas as pd
if __name__ == '__main__':
    df=pd.read_csv("EquipmentPerkEffects.csv")
    df.drop_duplicates("Name", keep='last', inplace=True, ignore_index=True)
    
    df.to_csv("EquipPerkProccessed.csv",index=False)