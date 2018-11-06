#encoding=utf-8
import MySQLdb
# mysql 连接工具

class MysqlDB:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.dbname = "horsehive"
        self.user = "root"
        self.password = "wsjia369X"
        self.charcode = "utf8"
        self.db = MySQLdb.connect(host = self.host,
                                  port = self.port,
                                  user = self.user,
                                  passwd = self.password,
                                  db = self.dbname,
                                  charset = self.charcode)

    # 解析item, 插入item数据到mysql中
    def insert(self, item, tb):
        try:
            names = ""
            values = ""
            for key in item.keys():
                names += key + ','
                values += '"{value}"'.format(value = item[key]) + ','
            names = names.rstrip(',')
            values = values.rstrip(',')

            sql = "insert into {tb}({names}) values({values})".format(names=names, values=values, tb=tb)
            # print(sql)
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
        except:
            print('insert raise error')
            self.db.rollback()

    def close(self):
        self.db.close()

