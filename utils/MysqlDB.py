import MySQLdb
# mysql 连接工具

class MysqlDB:
    def __init__(self):
        self.host = ""
        self.dbname = ""
        self.user = ""
        self.password = ""
        self.charcode = "utf-8"
        self.db = MySQLdb.connect(self.host,
                                  self.user,
                                  self.password,
                                  self.dbname,
                                  self.charcode)

    # 解析item, 插入item数据到mysql中
    def insert(self, item):
        try:
            names = ""
            values = ""
            for key in item.keys():
                names += key + ','
                values += item[key] + ','
            names = names.rstrip(',')
            values = values.rstrip(',')

            sql = "insert into table({names}) values({values})".format(names=names, values=values)

            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def close(self):
        self.db.close()

