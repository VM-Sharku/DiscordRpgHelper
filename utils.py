import re

KoreanPattern = re.compile("^[ㄱ-힣]+$")
def IsKorean(str):
    return KoreanPattern.match(str) != None