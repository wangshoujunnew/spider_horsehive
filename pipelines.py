# -*- coding: utf-8 -*-
from horsehivecomment.utils.MysqlDB import *

mysql = MysqlDB()

class HorsehivecommentPipeline(object):
    def process_item(self, item, spider):
        return item




class TagPipeline(object):
    def process_item(self, item, spider):
        mysql.insert(item)
        return item

class CommentPipeline(object):
    def process_item(self, item, spider):
        mysql.insert(item)
        return item



