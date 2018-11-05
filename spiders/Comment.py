# -*- coding: utf-8 -*-
from horsehivecomment.items import *
import json
import scrapy
from horsehivecomment.utils.Utils import *
# 解析每个评论链接,得到评论内容,写入到mysql中

class CommentSpider(scrapy.Spider):
    name = 'Comment'
    allowed_domains = ['www.mafengwo.cn']
    start_urls = []
    commentListUrlDict = {}

    commentListUrlPath = 'commentListUrl.txt'

    # 加载评论也链接到start_utls 中
    with open(commentListUrlPath, 'r', encoding='utf-8') as lines:
        for line in lines:
            line = line.strip()
            urlObj = json.loads(line)
            start_urls.append(urlObj['commentListUrl'])
            commentListUrlDict[urlObj['commentListUrl']] = urlObj['tagName']

    print('请求的url为>>>')
    print(start_urls)

    def parse(self, response):
        print('当前请求url:' + response.url)
        if not requestError.error(response):  # 请求状态为200
            print('正常请求')
            # print(response.text)
            html = (json.loads(response.text))['html']
            for element in scrapy.Selector(text=html).xpath(
                    '//div[@class="comm-item _j_comment_item"]/div[@class="txt"]'):
                item = CommentItem()
                item['content'] = element.xpath('text()').extract_first()

                item['tagName'] = CommentSpider.commentListUrlDict[response.url]

                # utils.itemToFile(item, 'commentDetail.txt')
                yield item


        else:
            print('请求失败')

