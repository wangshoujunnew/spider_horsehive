#encoding=utf-8
import MySQLdb
# mysql 连接工具

class MysqlDB:
    def __init__(self):
        self.host = "10.2.72.38"
        self.port = 3306
        self.dbname = "horsehive"
        self.user = "root"
        self.password = "123456"
        self.charcode = "utf8"
        self.db = MySQLdb.connect(host = self.host,
                                  port = self.port,
                                  user = self.user,
                                  passwd = self.password,
                                  db = self.dbname,
                                  charset = self.charcode)

        self.cursor = self.db.cursor()
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
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print('insert raise error')
            self.db.rollback()

    def close(self):
        self.db.close()

    def select(self, sql):
        """
        fetchall: r: tuple(tuple)
        """
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return list(data)


    def update(self, jsonObj, tb): 
        tmpStr = ''
        for key in jsonObj.keys():
            if key not in ['id'] and jsonObj[key] not in [None, "", 0]:
                tmpStr += "set {key} = '{value}',".format(key=key, value=jsonObj[key])
        tmpStr = tmpStr.rstrip(',')
        sql = "update {tb} {setStr} where id = {id}".format(tb=tb, id=jsonObj['id'], setStr=tmpStr)
        self.cursor.execute(sql)
        self.db.commit()
