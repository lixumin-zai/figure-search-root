import sqlite3
import uuid

class UserAlreadyExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            wechat_id TEXT NOT NULL UNIQUE,
            verification_code TEXT NOT NULL UNIQUE,
            usage_count INTEGER NOT NULL DEFAULT 15,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def create_user(self, wechat_id, verification_code):
        self.cursor.execute('SELECT * FROM users WHERE wechat_id = ? OR verification_code = ?', 
                        (wechat_id, verification_code))
        if self.cursor.fetchone() is not None:
            raise UserAlreadyExistsError("该用户已存在")

        self.cursor.execute('INSERT INTO users (wechat_id, verification_code) VALUES (?, ?)', (wechat_id, verification_code))
        self.conn.commit()

    def create_user_and_usage_count(self, wechat_id, verification_code, usage_count):
        self.cursor.execute('SELECT * FROM users WHERE wechat_id = ? OR verification_code = ?', 
                        (wechat_id, verification_code))
        if self.cursor.fetchone() is not None:
            raise UserAlreadyExistsError("该用户已存在")

        self.cursor.execute('INSERT INTO users (wechat_id, verification_code, usage_count) VALUES (?, ?, ?)', (wechat_id, verification_code, usage_count))
        self.conn.commit()

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def get_user_info_by_wechat_id(self, wechat_id):
        self.cursor.execute('SELECT * FROM users WHERE wechat_id = ?', (wechat_id,))
        return self.cursor.fetchone()

    def get_user_info_by_verification_code(self, verification_code):
        self.cursor.execute('SELECT * FROM users WHERE verification_code = ?', (verification_code,))
        return self.cursor.fetchone()  # 返回匹配的用户信息

    def reduce_usage_count(self, verification_code):
        self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
        current_count = self.cursor.fetchone()
        # print(current_count)
        if current_count and current_count[0] > 0:
            self.cursor.execute('UPDATE users SET usage_count = usage_count - 1 WHERE verification_code = ?', (verification_code,))
            self.conn.commit()
        return current_count[0] - 1
    
    def updata_by_user_id(self, user_id, wechat_id, verification_code, usage_count):
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        current_count = self.cursor.fetchone()
        print(current_count)
        if current_count and current_count[0] > 0:
            self.cursor.execute('UPDATE users SET wechat_id = ?, verification_code = ?, usage_count = ? WHERE id = ?', (wechat_id, verification_code, usage_count, user_id))
            self.conn.commit()
    
    def increase_usage_count(self, verification_code, number):
        self.cursor.execute('SELECT usage_count FROM users WHERE verification_code = ?', (verification_code,))
        current_count = self.cursor.fetchone()
        
        if current_count is not None:
            new_count = current_count[0] + number
            self.cursor.execute('UPDATE users SET usage_count = ? WHERE verification_code = ?', (new_count, verification_code))
            self.conn.commit()

    def delete_user(self, wechat_id):
        self.cursor.execute("DELETE FROM users WHERE wechat_id = ?", (wechat_id,))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


class RechargeCodeDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS rechargeCode (
            id INTEGER PRIMARY KEY,
            recharge_code TEXT NOT NULL UNIQUE,
            used_code TEXT,
            usage_count INTEGER NOT NULL DEFAULT 100
        )
        ''')
        self.conn.commit()

    def create_code(self):
        recharge_code = str(uuid.uuid4())
        self.cursor.execute('SELECT * FROM rechargeCode WHERE recharge_code = ?', 
                        (recharge_code, ))
        if self.cursor.fetchone() is not None:
            raise UserAlreadyExistsError("该用户已存在")

        self.cursor.execute('INSERT INTO rechargeCode (recharge_code) VALUES (?)', (recharge_code, ))
        self.conn.commit()
        return recharge_code

    def get_infos(self):
        self.cursor.execute('SELECT * FROM rechargeCode')
        return self.cursor.fetchall()

    def get_info_by_recharge_code(self, recharge_code):
        self.cursor.execute('SELECT * FROM rechargeCode WHERE recharge_code = ?', (recharge_code,))
        return self.cursor.fetchone()

    def get_info_by_used_code(self, used_code):
        self.cursor.execute('SELECT * FROM rechargeCode WHERE used_code = ?', (used_code,))
        return self.cursor.fetchone()  # 返回匹配的用户信息

    def used_code(self, recharge_code, used_code):
        info = self.get_info_by_recharge_code(recharge_code)
        cost_time = 0
        if info:
            cost_time = info[3]
        self.cursor.execute('UPDATE rechargeCode SET used_code = ?,usage_count = 0 WHERE recharge_code = ?', (used_code, recharge_code, ))
        self.conn.commit()
        return cost_time

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    import uuid
    # db = Database('test_0928.db')
    # # db.create_user('lixumin', 'lixumin')
    # # db.delete_user('cz71227669889')
    # # db.create_user('cz71227669889', 'cz71227669889')
    # # db.increase_usage_count("cz71227669889", 85)
    # # db.updata_by_user_id(1, "xrkuma", "bini", "52013149999")
    # for i in db.get_users():
    #     if i[1] == "xrkuma":
    #         print(i)
    # import uuid
    # # db.create_user('xrkuma', "bini")
    
    db = RechargeCodeDB("/root/project/figure_search/db/rechargecode.db")
    data = db.get_infos()
    for i in data:
        print(i)
    # # 查询用户信息
    db.close()



######. 跟新字段默认值
# db.cursor.execute('ALTER TABLE users RENAME TO old_users;')
# db.conn.commit()
# db.cursor.execute('''CREATE TABLE users (
#     id INTEGER PRIMARY KEY,
#     wechat_id TEXT NOT NULL UNIQUE,
#     verification_code TEXT NOT NULL UNIQUE,
#     usage_count INTEGER NOT NULL DEFAULT 15,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
# );''')
# db.conn.commit()

# db.cursor.execute("""INSERT INTO users (id, wechat_id, verification_code, usage_count, created_at)
#     SELECT id, wechat_id, verification_code, usage_count, created_at FROM old_users;""")
# db.conn.commit()
####