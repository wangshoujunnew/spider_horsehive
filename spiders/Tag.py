# -*- coding: utf-8 -*-
import math
import scrapy
from horsehivecomment.items import *
from scrapy.http.request.form import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector
from horsehivecomment.utils.Utils import *
import json
import re
# 爬取酒店详情页下面 每个6个topic 项目对应的评论链接
class TagSpider(scrapy.Spider):
    name = 'Tag'
    allowed_domains = ['www.mafengwo.cn']
    start_urls = []
    # 初始化 , 将所有hotel详情页的url加载到start_urls 中

    with open('E:/horsehivecomment/horsehivecomment/utils/HotelDetailUrl.txt', 'r', encoding='utf-8') as lines:
        for line in lines:
            line = line.strip()
            if line.startswith('--') or line.__len__() <= 0 or line.startswith('下一页点击'):
                pass
            else:
                start_urls.append(line)

    print('start_urls>>>>>>>>>>>>>')
    print(start_urls)

    def parse(self, response):  # 得到酒店详情页的6个标签
        for tag in response.xpath('//a[@class="_j_comment_keyword"]'):  # **
            item = TagItem()

            item['dataId'] = tag.xpath('@data-id').extract_first()  # *
            item['hotelId'] = re.findall('hotel/(\d+).html', response.url)[0]  # *
            item['dataType'] = tag.xpath('@data-type').extract_first()  # *
            item['num'] = tag.xpath('i/text()').extract_first()
            item['totalNum'] = tag.xpath('span/em/text()').extract_first()  # * 这个标签总点评量 / 10,可以得到页数
            item['tagName'] = tag.xpath('strong/text()').extract_first()  # *
            print(">>>>>>>>>>")
            # 生成url
            # var
            # B = {
            #     poi_id: 40046,
            #     type: 0,
            #     keyword_id: 105840529,
            #     page: 1,
            # };
            # 生成每个标签页下面的所有点评list页链接
            if item['totalNum'] and int(item['totalNum']) > 0:
                pageTotal = int(math.ceil(float(item['totalNum']) / 10))
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
                                JSON.stringify(B)
                                return JSON.stringify(B)
                                ''' % (item['hotelId'], str(0), item['dataId'], str(page))  # 先默认要一个page = 1的
                    print('执行js>>>>')
                    # print(script)

                    # poi_id=40046&type=0&keyword_id=0&page=2
                    result = utils.getJsEnvironment( script=script) # url=jsurl,

                    parameter = json.loads(result)
                    writeUrl = ''
                    size = list(parameter.keys()).__len__()
                    for index, key in zip(range(0, size), parameter.keys()):
                        if index >= size - 1:
                            writeUrl += key + '=' + str(parameter[key])
                        else:
                            writeUrl += key + '=' + str(parameter[key]) + '&'

                    writeUrl = commentListUrl + writeUrl
                    writeData = {'tagName': item['tagName'], 'commentListUrl': writeUrl}

                    # utils.writeToFile('commentListUrl.txt',
                    #                  text=json.dumps(writeData).encode('utf-8').decode('unicode_escape'), append=True)
                    yield item # 将写入文件的方式改成写入到mysql中
            else:
                pass

# comment_list 页面
# poi_id:40388 酒店ID
# type 0 data-type="1"
# keyword_id:179049854  data-id="106777699"
# page:1
# _ts:1540480690525
# _sn:6771459b45

