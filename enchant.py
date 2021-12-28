from enum import Enum
import random

class EnchantResult(Enum):
    SUCCESS = 0
    NORMAL = 1
    FAIL = 2
    BREAK = 3
    def __str__(self):
        if self == EnchantResult.SUCCESS:
            return "성공"
        elif self == EnchantResult.NORMAL:
            return "실패"
        elif self == EnchantResult.FAIL:
            return "실패"
        elif self == EnchantResult.BREAK:
            return "실패"

class EnchantChance():
    def __init__(self,successRate=250,normalRate=250,failRate=250,breakRate=250):
        if successRate + normalRate + failRate + breakRate != 1000:
            raise ValueError(f"Sum of chances is not 1000. {successRate + normalRate + failRate + breakRate}")
        self.__Success = successRate
        self.__Normal = normalRate
        self.__Fail = failRate
        self.__Break = breakRate

    def SuccessLimit(self):
        return self.__Success

    def NormalLimit(self):
        return self.__Success + self.__Normal

    def FailLimit(self):
        return self.__Success + self.__Normal + self.__Fail
    
    def BreakLimit(self):
        return self.__Success + self.__Normal + self.__Fail + self.__Break

EnchantChanceTable = {
    0:EnchantChance(950,50,0,0),
    1:EnchantChance(900,100,0,0),
    2:EnchantChance(850,150,0,0),
    3:EnchantChance(850,150,0,0),
    4:EnchantChance(800,200,0,0),
    5:EnchantChance(750,250,0,0),
    6:EnchantChance(700,300,0,0),
    7:EnchantChance(650,350,0,0),
    8:EnchantChance(600,400,0,0),
    9:EnchantChance(550,450,0,0),
    10:EnchantChance(500,500,0,0),
    11:EnchantChance(450,0,550,0),
    12:EnchantChance(400,0,594,6),
    13:EnchantChance(350,0,637,13),
    14:EnchantChance(300,0,686,14),
    15:EnchantChance(300,679,0,21),
    16:EnchantChance(300,0,679,21),
    17:EnchantChance(300,0,679,21),
    18:EnchantChance(300,0,672,28),
    19:EnchantChance(300,0,672,28),
    20:EnchantChance(300,630,0,70),
    21:EnchantChance(300,0,630,70),
    22:EnchantChance(30,0,776,194),
    23:EnchantChance(20,0,686,294),
    24:EnchantChance(10,0,594,396),
}

Blacklist = {
}

SuccessMessage = [
    "이/가 찬란한 빛으로 빛납니다.",
]

NormalMessage = [
    "은/는 아무런 변화가 없어 보입니다.",
]

FailMessage = [
    "은/는 다행히 파괴되지는 않았습니다. 하지만 빛이 바랬습니다...",
]

BreakMessage = [
    "은/는 강렬한 빛을 내고 흔적도 없이 사라졌습니다.",
    "이/가 산산조각 났습니다.",
    "은/는 한순간 빛나는 듯 하더니 말라비틀어졌습니다.",
    "은/는 격렬한 폭음과 함께 폭발했습니다.",
    "에서 찬란한 빛이 나는 듯 했지만, 햇빛이 눈에 반사된 것이었습니다. 남은건 잡다한 부스러기 뿐입니다.",
]

def enchant_internal(level):
    if level not in EnchantChanceTable and level > sorted(EnchantChanceTable.keys(), reverse=True)[0]:
        level = sorted(EnchantChanceTable.keys(), reverse=True)[0]
    enchantChance = EnchantChanceTable[level]
    chance = random.randrange(0, 1000)
    if chance < enchantChance.SuccessLimit():
        return EnchantResult.SUCCESS
    elif chance < enchantChance.NormalLimit():
        return EnchantResult.NORMAL
    elif chance < enchantChance.FailLimit():
        return EnchantResult.FAIL
    elif chance < enchantChance.BreakLimit():
        return EnchantResult.BREAK
    else:
        raise ValueError(f"chance: {chance}, chance sum: {enchantChance.BreakLimit()}")