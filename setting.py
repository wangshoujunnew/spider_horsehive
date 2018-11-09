BOT_NAME = 'horsehivecomment'
SPIDER_MODULES = ['horsehivecomment.spiders']
NEWSPIDER_MODULE = 'horsehivecomment.spiders'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1
SPIDER_MIDDLEWARES = {
   'horsehivecomment.middlewares.HorsehivecommentSpiderMiddleware': 543,
}
DOWNLOADER_MIDDLEWARES = {
   'horsehivecomment.middlewares.HorsehivecommentDownloaderMiddleware': 543,
}
ITEM_PIPELINES = {
   'horsehivecomment.pipelines.CommentPipeline': 300,
   'horsehivecomment.pipelines.TagPipeline': 299,
   'horsehivecomment.pipelines.HorsehivecommentPipeline': 500,
}
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
COOKIES_ENABLED = True
TELNETCONSOLE_ENABLED = False 
FEED_EXPORT_ENCODING = 'utf-8' 
AUTOTHROTTLE_ENABLED = True 
