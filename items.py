import scrapy


class HorsehivecommentItem(scrapy.Item):
    pass

# 酒店下的6个标签对应的分页url
class TagItem(scrapy.Item):
    tag_name = scrapy.Field()           # 标签名称
    hotel_id = scrapy.Field()           # 酒店ID
    comment_urlpage = scrapy.Field()    # 分页之后的评论url接口


# 评论Item
class CommentItem(scrapy.Item):
    tag_name = scrapy.Field()           # 评论所属于的标签
    content = scrapy.Field()            # 评论内容
    star = scrapy.Field()               # 评论的星数

