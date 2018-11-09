# -*- coding: utf-8 -*-
import math
from horsehivecomment.items import *
from horsehivecomment.utils.Utils import *
import json
import scrapy
import re
import copy

commentListUrl = 'http://www.mafengwo.cn/hotel/info/comment_list?'  # 评论列表页的前缀


# 爬取酒店详情页下面 每个6个topic 项目对应的评论链接
class TagSpider(scrapy.Spider):
    name = 'Tag'
    allowed_domains = ['www.mafengwo.cn']
    urlData = []
    # 初始化 , 从数据库中拿出10个来做爬虫
    mysql = MysqlDB()

    def start_requests(self):
        while (True):
            if TagSpider.urlData.__len__() <= 0:
                TagSpider.urlData = mysql.select('select * from hotel where flag = 0 limit 100',
                                                 {'id': '', 'hotel_id': '', 'detail_url': '', 'flag': '',
                                                  'city_id': ''})

                if not TagSpider.urlData:
                    break

                for url in copy.deepcopy(TagSpider.urlData):
                    yield scrapy.Request(url=url['detail_url'], callback=self.parse)
                    tmpurl = {}
                    tmpurl['id'] = url['id']
                    tmpurl['flag'] = '1'
                    mysql.update(tmpurl, 'hotel')
                    TagSpider.urlData.remove(url)

    def parse(self, response):  # 得到酒店详情页的6个标签
        for tag in response.xpath('//a[@class="_j_comment_keyword"]'):  # **
            tmpJson = {}
            tmpJson['dataId'] = tag.xpath('@data-id').extract_first()  # *
            tmpJson['hotel_id'] = re.findall('hotel/(\d+).html', response.url)[0]  # *
            tmpJson['dataType'] = tag.xpath('@data-type').extract_first()  # *
            tmpJson['num'] = tag.xpath('i/text()').extract_first()
            tmpJson['totalNum'] = tag.xpath('span/em/text()').extract_first()  # * 这个标签总点评量 / 10,可以得到页数
            tmpJson['tag_name'] = tag.xpath('strong/text()').extract_first()  # *
            # var
            # B = {
            #     poi_id: 40046,
            #     type: 0,
            #     keyword_id: 105840529,
            #     page: 1,
            # };
            # 生成每个标签页下面的所有点评list页链接
            if tmpJson['totalNum'] and int(tmpJson['totalNum']) > 0:
                pageTotal = int(math.ceil(float(tmpJson['totalNum']) / 10))
                # 现在马蜂窝上只提供200条点评的内容
                if pageTotal > 20:
                    pageTotal = 20
                for page in range(1, pageTotal + 1):
                    script = '''
                    var B = { 
                        poi_id: %s,
                        type: %s,
                        keyword_id: %s,
                        page: %s,
                    };
                    B._ts = new Date().getTime();
                    var z = window.__MFW_MODULE__.hotel.SignUgifily.getSignV2($.extend({}, B));
                    B._sn = z 
                    return JSON.stringify(B)
                    ''' % (tmpJson['hotel_id'], str(0), tmpJson['dataId'], str(page))
                    result = utils.getJsEnvironment(script=script)  # url=jsurl,

                    parameter = json.loads(result)
                    comment_urlpage = ''
                    for key in parameter.keys():
                        comment_urlpage += key + '=' + str(parameter[key]) + '&'

                    comment_urlpage = comment_urlpage.rstrip('&')

                    comment_urlpage = commentListUrl + comment_urlpage

                    item = TagItem()
                    item['tag_name'] = tmpJson['tag_name']
                    item['comment_urlpage'] = comment_urlpage
                    item['hotel_id'] = tmpJson['hotel_id']
                    yield item  #
            else:
                pass

