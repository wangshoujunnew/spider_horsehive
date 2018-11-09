# spider_horsehive
# 需要环境 >>>>>>>>>>>>>>>>>>>
1: selenium
2: scrapy

# 程序启动 >>>>>>>>>>>>>>>>>>>>
1: 建立项目 scrapy startproject hornet_nest
2: 建立抓取两个类 
  scrapy gengspider Tag:      标签抓取类     
  scrapy gengspider Comment:  评论抓取类
  
3: 将对于的文件替换到自己的项目中
4: 配置数据库 utils.MysqlDB
5: 抓取某个城市下的门店 python utils/HotelDetailUrlGetBySelenium.py
6: 抓取酒店下标签对应的url: scrapy crawl Tag
7: 抓取Tag中的url的评论内容: scrapy crawl Comment
