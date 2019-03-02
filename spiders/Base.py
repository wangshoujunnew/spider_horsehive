# -*- coding: utf-8 -*-
from horsehivecomment.items import *
import json
import scrapy
from horsehivecomment.utils.Utils import *
import copy
# 模版

# 解析每个评论链接,得到评论内容,写入到mysql中

class BaseSpider(scrapy.Spider):
    name = 'Comment'
    allowed_domains = ['www.mafengwo.cn']
    start_url = []
    has_spider_url = []
    # 初始化 , 从数据库中拿出10个来做爬虫
    mysql = MysqlDB()
    
    # 提取没有爬的URL
    def start_requests(self):
        while (True):
            if len(BaseSpider.start_url) <= 0:    		# 数据库中或者文件中取出没有爬取的url放入到start_url中, 每次爬取100个url
            											# 最好改成文件中, 比较方便
                BaseSpider.start_url = mysql.select('select * from tag_2 where flag = 0 limit 100',
                                                     {'id': '', 'tag_name': '', 'hotel_id': '', 'comment_urlpage': '',
                                                      'flag': ''})

                for url in copy.deepcopy(BaseSpider.start_url):
                    yield scrapy.Request(url=url, callback=self.parse) # 请求url的内容
                    has_spider_url.append(url)          # 将url添加到已经爬取的队列中

    def parse(self, response):
        if response.status == 200:                      # 请求状态为200
            html = (json.loads(response.text))['html']  # 建议使用pyquery选择
            item = Item()
            item['?'] = 0
            yield item
        else:
            print('请求失败')
