class StatusError(Exception):
    pass

class Character():
    def __init__(self):
        self.Name=""
        self.Appearance=[]
        self.Inventory=[]
        self.Buffs=[]
        self.__Health=0
        self.MaxHealth=0
        self.Equipment=[]

    @property
    def Health(self):
        return self.__Health
    
    @Health.setter
    def Health(self, newHP):
        if newHP < 0:
            newHP = 0
        self.__Health = newHP

class DWCharacter(Character):
    def __init__(self):
        self.Race=""            # 종족
        self.Alignment=""       # 성향
        self.Strength=0         # 근력
        self.Dexterity=0        # 민첩
        self.Constitution=0     # 체력
        self.Wisdom=0           # 
        self.Intelligence=0     # 
        self.Charisma=0         # 
        self.MaxWeight=0        # 
    
    @property
    def Weight(self):
        weight = 0
        for item in self.Inventory:
            weight += item.Weight
        for equip in self.Equipment:
            weight += equip.weight
        if weight < 0:
            raise StatusError("Weight cannot be less than 0.")
        if weight > self.MaxWeight:
            raise StatusError("Weight cannot be greater than max weight")
        return weight
    
    @Weight.setter
    def Weight(self, Value):
        pass
    
    def Validate(self):
        if self.ValidateStats() == False:
            return False

    def ValidateStats(self):
        if self.Strength < 0 or self.Strength > 25:
            return False
        if self.Dexterity < 0 or self.Dexterity > 25:
            return False
        if self.Constitution < 0 or self.Constitution > 25:
            return False
        if self.Wisdom < 0 or self.Wisdom > 25:
            return False
        if self.Intelligence < 0 or self.Intelligence > 25:
            return False
        if self.Charisma < 0 or self.Charisma > 25:
            return False
        return True

    def Reset(self):
        return
    
    def save(self):
        return
        
    def load(self):
        return