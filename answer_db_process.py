import sqlite3
import os

class AnswerImageDB:
    def __init__(self, db_path='answer.db', use_blob=True):
        """
        初始化 ImageStorage 类

        :param db_path: 数据库路径
        :param use_blob: 是否使用 BLOB 存储图片 (True 为存储图片到数据库, False 为仅存储路径)
        """
        self.db_path = db_path
        
        # 创建数据库连接
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY,
                image BLOB
            )
        ''')

    def search_all_image(self):
        """
        搜索所有题库数据
        """
        self.cursor.execute("SELECT * FROM images")
        return self.cursor.fetchall()

    def insert_image(self, image_bytes):
        """
        添加所有题库数据
        """
        self.cursor.execute("INSERT INTO images (image) VALUES (?)", (image_bytes,))
        self.conn.commit()

    def retrieve_image(self, image_id):
        """
        通过ID 匹配答案题目
        """
        self.cursor.execute("SELECT image FROM images WHERE id=?", (image_id,))
        if self.cursor.fetchone()[0]:
            image_bytes = self.cursor.fetchone()[0]
        else:
            return b''
        return image_bytes

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

    def delete_image(self, image_id):
        """
        从数据库中删除图片或图片路径
        """
        self.cursor.execute("DELETE FROM images WHERE id=?", (image_id,))
        self.conn.commit()

if __name__ == "__main__":
    import os
    answer_image_db = AnswerImageDB("/root/project/figure_search_root/answer.db")
    # root_path = "/root/project/figure_search_root/image"
    # for i in sorted(os.listdir("/root/project/figure_search_root/image"), key=lambda x:int(x.split(".")[0])):
    #     # print(i)
    #     with open(f"{root_path}/{i}", "rb") as f:
    #         image_bytes = f.read()
    #         answer_image_db.insert_image(image_bytes)
    
    data = answer_image_db.search_all_image()
    for image_bytes in data:
        print(image_bytes[0])

    
    # with open("/root/project/figure_search_root/database/c96d7e57-8b3a-4651-9ab6-407673de4ae11721632702415.png", "rb") as f:
    #     answer_image_db.insert_image(f.read())
    # answer_image_db = AnswerImageDB("./answer.db")
    # data = answer_image_db.search_all_image()
    # for image_bytes in data:
    #     with open("1.png", "wb") as f:
    #         f.write(image_bytes[1])
    #     break