import datetime
import json
import random
import selenium.webdriver as WebDriver
import time
from horsehivecomment.utils.MysqlDB import *

mysql = MysqlDB()

class Utils(object):
    driver = WebDriver.Chrome()
    jsurl = 'http://www.mafengwo.cn/hotel/40388.html?iMddid=10065'  # 为了得到js的执行环境
    driver.get(jsurl)

    time.sleep(20)

    def __init__(self):
        self.ipLines = []
        self.ip_proxy_file = ""
        self.jsurl = None


    def writeToFile(self, filePath, text, append=False):  # 写入文件的方式默认是覆盖
        writeType = 'w'
        if append:
            writeType = 'a+'
        with open(filePath, writeType, encoding="UTF-8") as file:
            file.writelines(text + '\n')

    def itemToFile(self, item, path):  # item 写入到file文件中
        itemDict = {}
        for key in item.keys():
            itemDict[key] = item[key]
        with open(path, 'a+', encoding='utf-8') as file:
            file.writelines(json.dumps(itemDict).encode('utf-8').decode('unicode_escape') + '\n')


    def getJsEnvironment(self, script):
        try:
            return self.driver.execute_script(script=script)
        except:
            print('js代码执行error >>>>>>>>> ')
            return None

    def close(self):
        # 关闭浏览器
        self.driver.close()


# 自定义日志处理
class LoggerMy(object):
    def __init__(self):
        self.logPath = 'SpiderLogMy.txt'

    def info(self, text, level='info'):
        newText = str(datetime.datetime.now()) + " : " + level + " : " + text
        with open(self.logPath, 'a+', encoding='utf-8') as f:
            f.writelines(newText + '\n')


utils = Utils()
loggerMy = LoggerMy()


# utils.getJsEnvironment('http://www.baidu.com', 'console.log("hello world")')
# time.sleep(20)
# utils.close()

# 记录错误请求处理
class RequestErrorHander(object):
    def error(self, response):
        if response.status == 200:
            return False
        else:
            text = '请求出错,状态码' + str(response.status)
            loggerMy.info(text, 'status error')
            return True


requestError = RequestErrorHander()

