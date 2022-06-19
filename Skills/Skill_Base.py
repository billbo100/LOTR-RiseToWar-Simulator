'''
Created on Jun 17, 2022

@author: Billy Culver
'''


class Skill(object):
    def __init__(self,name,level,bonus=''):
        self.name=name
        self.bonus=bonus
        self.level=level
        self.max_level=7
    
        if(bonus):
            if(bonus.Title):
                self.max_level=15
            
    def get_skill_Descript(self):
        return None
    def get_cooldown(self):
        return ''
    def __str__(self, *args, **kwargs):
        return_str=self.name+'(%d/%d) %s\n'%(self.level,self.max_level,self.get_cooldown())
        if(self.get_skill_Descript()):
            return_str+=self.get_skill_Descript()
        return return_str



        

class Damage_Skill(Skill):
    def __init__(self,name,Target,percent_per_level,cooldown,DamageType,level=1,bonus=None,prioritize=None,select_target=None,pursuit=False,Rush=False):
        
        self.Target=Target
        self.percent_per_level=percent_per_level
        self.cooldown=cooldown
        self.prioritize=prioritize
        self.pursuit=pursuit
        self.Rush=Rush
        self.DamageType=DamageType
        self.select_target=select_target
        
        
        self.cooldown=cooldown
        Skill.__init__(self, name, level=level, bonus=bonus)
    def get_skill_Descript(self):
        if(self.Rush):
            rush_mod='[Rush]'
        else:
            rush_mod=''
        if(type(self.Target)==int):
            tg='[Against %d Enemy Target(s)]'%self.Target
        else:
            tg='[Against Enemy Target with the %s]'%self.Target
        bonus_str=''    
        if(self.bonus):
            bonus_str=self.bonus.get_Bonus(self.level)
        return "%s%s Deals %.1f%% %s Damage. %s"%(rush_mod,tg,self.percent_per_level*self.level,self.DamageType,bonus_str)
    def get_cooldown(self):
        return "Cooldown: %d turns"%(self.cooldown)
        















