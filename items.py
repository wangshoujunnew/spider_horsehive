import scrapy


class HorsehivecommentItem(scrapy.Item):
    pass

class TagItem(scrapy.Item):
    num = scrapy.Field()
    tagName = scrapy.Field()
    hotelId = scrapy.Field()
    dataType = scrapy.Field()
    dataId = scrapy.Field()
    totalNum = scrapy.Field()

class IpItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()

class CommentItem(scrapy.Item):
    tagName = scrapy.Field()
    content = scrapy.Field()

