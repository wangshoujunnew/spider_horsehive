import time
import random
import selenium.webdriver as WebDriver
from scrapy.selector import Selector
# 通过浏览器的方式爬取马蜂窝北京的酒店ID(进入酒店详情页的链接)

def writeToFile(text, path='HotelDetailUrl.txt'):
    with open(path, 'a+', encoding='utf-8') as f:
        f.writelines(text + '\n')


def parseHtml(html):
    selector = Selector(text=html)
    for element in selector.xpath('//h3/a[@class="_j_hotel_info_link"]'):
        urlText = 'http://www.mafengwo.cn' + element.xpath('@href').extract_first()
        writeToFile(urlText)
    return None


def isElementExists(driver, xpath):
    try:
        element = driver.find_element_by_xpath(xpath)
        return element
    except:
        return False


def randomSleep():
    # 随机睡眠1-2秒
    time.sleep(random.randrange(1, 5))


driver = WebDriver.Chrome()
driver.get('http://www.mafengwo.cn/hotel/10099/')  # 北京
time.sleep(20)

html = driver.page_source

parseHtml(html)

pageTotal = int(Selector(text=html).xpath('//div[@id="list_paginator"]/span/span/text()').extract_first())  # 总页数
nextPage = isElementExists(driver, '//a[@class="ti _j_pageitem prev"][last()]')

curPage = 1

while nextPage and curPage <= pageTotal:
    writeToFile('下一页点击:' + str(curPage) + '>>>>>>>>>')
    nextPage.click()  # 下一页点击
    parseHtml(driver.page_source)
    curPage += 1
    randomSleep()
    nextPage = isElementExists(driver, '//a[@class="ti _j_pageitem prev"][last()]')  # 继续查看下一页按钮是否存在

driver.close()

