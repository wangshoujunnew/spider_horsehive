# -*- coding: utf-8 -*-

from scrapy import signals
from horsehivecomment.utils.Utils import *
import requests
# 建立IP代理

class HorsehivecommentSpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):

        pass

    def process_start_requests(self, start_requests, spider):


        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HorsehivecommentDownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        ip = requests.get('http://10.2.3.100:5010/get').text
        print('使用代理 = {}. log by sjw ... '.format(ip))
        request.meta['proxy'] = 'http://' + ip  # + proxy_ip # '118.190.95.35:9001'
        return None

    def process_response(self, request, response, spider):
        if response.status == 200:
            return response

        elif response.status == 404::  # 只删除404状态码的代理
            ip = request.meta['proxy']
            ip = ip[ip.index('//') + 2:] # print('http://10.2.3.100:5010/delete?proxy=' + ip)
            requests.get('http://10.2.3.100:5010/delete?proxy=' + ip)
            print('reomve ip from proxy pool = {}. log by sjw ... '.format(ip))
          
        # 建立新代理
        request.meta['proxy'] = requests.get('http://10.2.3.100:5010/get').text
        return request

    def process_exception(self, request, exception, spider):

        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

