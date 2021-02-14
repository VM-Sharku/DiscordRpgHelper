import sqlite3

# use sqlite
class EnchantDB():
    Connection = sqlite3.connect("enchant.db")
    def __init__(self):
        self.cursor = EnchantDB.Connection.cursor()

        # 강화 순위 DB 테이블
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS enchant_record (
                                USER_ID INTEGER PRIMARY KEY,
                                HIGHEST_ITEM TEXT,
                                HIGHEST_ITEM_LEVEL INTEGER
                                );''')
        
        # 강화 진행정보 DB 테이블
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS enchant_processing (
                                USER_ID INTEGER PRIMARY KEY,
                                ITEM_NAME TEXT,
                                ITEM_LEVEL INTEGER,
                                HIGHEST_ITEM_LEVEL INTEGER,
                                ENCHANT_COUNT INTEGER
                                );''')

#db = EnchantDB()
#db.cursor.execute(f"INSERT INTO enchant_record VALUES (2113,'',0)")
#db.Connection.commit()
#db.cursor.execute(f"SELECT * FROM enchant_record WHERE USER_ID=2113")
#
#print(db.cursor.f())