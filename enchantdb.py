import sqlite3

# use sqlite
class EnchantDB():
    Connection = sqlite3.connect("enchant.db")
    def __init__(self):
        self.cursor = EnchantDB.Connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS enchant_record (
                                USER_ID INTEGER PRIMARY KEY,
                                HIGHEST_ITEM TEXT,
                                HIGHEST_ITEM_LEVEL INTEGER
                                );''')

#db = EnchantDB()
#db.cursor.execute(f"INSERT INTO enchant_record VALUES (2113,'',0)")
#db.Connection.commit()
#db.cursor.execute(f"SELECT * FROM enchant_record WHERE USER_ID=2113")
#
#print(db.cursor.f())