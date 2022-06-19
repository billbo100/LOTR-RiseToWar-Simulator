




from Skills.Skill_Base import Bonus, Damage_Skill


class Anduril(Damage_Skill):
    def __init__(self,level=1):
        B=Bonus(Title="Might +15")
        Damage_Skill.__init__(self, name="Anduril",level=level,Target=2, percent_per_level=20, cooldown=2, DamageType="Physical",bonus=B)
        
class Cull_the_Weak(Damage_Skill):
    def __init__(self,level=1):
        Damage_Skill.__init__(self, name="Cull the Weak",level=level,Target="Lowest Defense", percent_per_level=30, cooldown=1, DamageType="Physical")

class Raid(Damage_Skill):        
    def __init__(self,level=1):
        bonus=Bonus(baseChance=0.5, BonusType="Physical", effectPerLevel=240/7)
        Damage_Skill.__init__(self, name="Raid",level=level,Target=1, percent_per_level=240/7, cooldown=2,Rush=True, DamageType="Physical",bonus=bonus)

class Precise_Blow(Damage_Skill):        
    def __init__(self,level=1):
        bonus=Bonus(BonusType="Pursuit")
        Damage_Skill.__init__(self, name="Precise Blow",level=level,Target=1, percent_per_level=40, cooldown=1, DamageType="Physical",bonus=bonus)
       
        
        
        
        
