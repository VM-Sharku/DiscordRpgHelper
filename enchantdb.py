from enchant import EnchantResult
import sqlite3
from item import Item

# use sqlite
class EnchantDB():
    Connection = sqlite3.connect("enchant.db")
    SchemaName_rank = "enchant_rank"
    SchemaName_item = "enchant_item"
    def __init__(self):
        self.cursor = EnchantDB.Connection.cursor()
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {EnchantDB.SchemaName_rank} (
                                ITEM_NAME TEXT PRIMARY KEY,
                                UID INTEGER,
                                HIGHEST_LEVEL INTEGER,
                                ENCHANT_COUNT INTEGER
                                );''')
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {EnchantDB.SchemaName_item} (
                                ITEM_NAME TEXT PRIMARY KEY,
                                LEVEL INTEGER,
                                ENCHANT_COUNT INTEGER,
                                LAST_RESULT INTEGER,
                                CHANCETIME INTEGER
                                );''')
    def getRanking(self, itemname):
        self.cursor.execute(f"SELECT * FROM {EnchantDB.SchemaName_rank} WHERE ITEM_NAME='{itemname}';")
        result = self.cursor.fetchone()
        if result == None:
            return None
        return result
    def getRankings(self, size=10):
        self.cursor.execute(f"SELECT * FROM {EnchantDB.SchemaName_rank} ORDER BY HIGHEST_LEVEL DESC;")
        return self.cursor.fetchmany(size)
    def addRanking(self, itemname, uid, highestLevel, enchantCount):
        self.cursor.execute(f"INSERT INTO {EnchantDB.SchemaName_rank} VALUES ('{itemname}',{uid},{highestLevel},{enchantCount});")
        self.Connection.commit()
    def updateRanking(self, itemname, uid, highestLevel, enchantCount):
        self.cursor.execute(f'''UPDATE {EnchantDB.SchemaName_rank}
                                SET UID={uid}, HIGHEST_LEVEL={highestLevel}, ENCHANT_COUNT={enchantCount}
                                WHERE ITEM_NAME='{itemname}';''')
        self.Connection.commit()
    def getItem(self, itemname):
        self.cursor.execute(f"SELECT * FROM {EnchantDB.SchemaName_item} WHERE ITEM_NAME='{itemname}';")
        result = self.cursor.fetchone()
        if result == None:
            return None
        _, level, enchant_count, last_result, chancetime = result
        item = Item(itemname)
        item.Level = level
        item.EnchantCount = enchant_count
        item.ChanceTime = chancetime != 0
        item.LastEnchantResult = EnchantResult(last_result)
        return item
    def getItems(self):
        self.cursor.execute(f"SELECT * FROM {EnchantDB.SchemaName_item}")
        items = self.cursor.fetchall()
        result = []
        for itemname, level, enchant_count, last_result, chancetime in items:
            item = Item(itemname)
            item.Level = level
            item.EnchantCount = enchant_count
            item.LastEnchantResult = EnchantResult(last_result)
            item.ChanceTime = chancetime != 0
            result.append(item)
        return result
    def addItem(self, item):
        self.cursor.execute(f"INSERT INTO {EnchantDB.SchemaName_item} VALUES ('{item.Name}',{item.Level},{item.EnchantCount},{item.LastEnchantResult.value},{int(item.ChanceTime)});")
        self.Connection.commit()
    def updateItem(self, item):
        self.cursor.execute(f'''UPDATE {EnchantDB.SchemaName_item}
                                SET LEVEL={item.Level}, ENCHANT_COUNT={item.EnchantCount},LAST_RESULT={item.LastEnchantResult.value},CHANCETIME={int(item.ChanceTime)}
                                WHERE ITEM_NAME='{item.Name}';''')
        self.Connection.commit()
    def removeItem(self, itemname):
        self.cursor.execute(f"DELETE FROM {EnchantDB.SchemaName_item} WHERE ITEM_NAME='{itemname}';")
        self.Connection.commit()