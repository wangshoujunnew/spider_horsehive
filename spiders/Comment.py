# -*- coding: utf-8 -*-
from horsehivecomment.items import *
import json
import scrapy
from horsehivecomment.utils.Utils import *
import copy


# 解析每个评论链接,得到评论内容,写入到mysql中

class CommentSpider(scrapy.Spider):
    name = 'Comment'
    allowed_domains = ['www.mafengwo.cn']
    commentListUrlDict = {}  # 存储url对应的tag_name
    urlData = []
    # 初始化 , 从数据库中拿出10个来做爬虫
    mysql = MysqlDB()
    
    # 提取没有爬的URL
    def start_requests(self):
        while (True):
            if CommentSpider.urlData.__len__() <= 0:
                CommentSpider.urlData = mysql.select('select * from tag_2 where flag = 0 limit 100',
                                                     {'id': '', 'tag_name': '', 'hotel_id': '', 'comment_urlpage': '',
                                                      'flag': ''})
                if not CommentSpider.urlData:
                    break

                for line in CommentSpider.urlData:
                    CommentSpider.commentListUrlDict[line['comment_urlpage']] = line['tag_name']

                for url in copy.deepcopy(CommentSpider.urlData):
                    yield scrapy.Request(url=url['comment_urlpage'], callback=self.parse)
                    tmpurl = {}
                    tmpurl['id'] = url['id']
                    tmpurl['flag'] = '1'
                    mysql.update(tmpurl, 'tag_2')
                    CommentSpider.urlData.remove(url)

    def parse(self, response):
        if not requestError.error(response):  # 请求状态为200
            html = (json.loads(response.text))['html'] # 建议使用pyquery选择
            
            for element in scrapy.Selector(text=html).xpath(
                    '//div[@class="comm-item _j_comment_item"]'):
                item = CommentItem()
                item['content'] = element.xpath('div[@class="txt"]/text()').extract_first()
                item['star'] = element.xpath('div[@class="comm-meta"]/span/@class').extract_first()
                item['star'] = item['star'][-1]
                item['tag_name'] = CommentSpider.commentListUrlDict[response.url]
                yield item
        else:
            print('请求失败')

