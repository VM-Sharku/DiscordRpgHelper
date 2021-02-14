from enchant import EnchantResult

class Item():
    def __init__(self, name="아이템"):
        self.Name = name
        self.__Level = 0
        self.HighestLevel = 0
        self.__EnchantCount = 0
        self.__Weight = 0
        self.__Price = 0
        self.LastEnchantResult = EnchantResult.SUCCESS
        self.ChanceTime = False
    @property
    def Level(self):
        return self.__Level
    @Level.setter
    def Level(self, newLevel):
        self.__Level = newLevel
    def Enchant(self, mod):
        if self.__Level + mod < 0:
            self.__Level = 0
            return
        self.__Level += mod
        if self.__Level > self.HighestLevel:
            self.HighestLevel = self.__Level
    @property
    def EnchantCount(self):
        return self.__EnchantCount
    def IncreaseEnchantCount(self):
        self.__EnchantCount += 1
    @property
    def Weight(self):
        return self.__Weight
    @Weight.setter
    def Weight(self, newWeight):
        if newWeight < 0:
            raise ValueError(f"Weight of {self.Name} cannot be less than 0.")
        self.__Weight = newWeight
    @property
    def Price(self):
        return self.__Price
    @Price.setter
    def Price(self, newPrice):
        self.__Price = newPrice