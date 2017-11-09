# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider
from bs4 import BeautifulSoup
import sys
import os
from getbooklist.items import DoubanItem
from scrapy.exceptions import DropItem
reload(sys)
sys.setdefaultencoding("utf-8")

class DoubanSpider(Spider):
    name = "Douban"
    download_delay = 1 #减慢爬取速度
    allowed_domains = ["douban.com"]
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36" }

    URL = "https://www.douban.com/doulist/1264675/?start={start}"

    def start_requests(self):
        index = 0
        for i in range(1,20):
            yield scrapy.Request(self.URL.format(start=index), headers = self.headers)
            index += 25

    #是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。
    #该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象
    def parse(self, response):
        if response.status == 404:
            raise CloseSpider("The page doesn't exist")

        soup = BeautifulSoup(response.body)
        # os._exit(0) #直接退出, 不抛异常, 不执行相关清理工作. 常用在子进程的退出
        # #sys.exit() #退出程序引发SystemExit异常, 可以捕获异常执行些清理工作. n默认值为0, 表示正常退出. 其他都是非正常退出. 还可以sys.exit("sorry, goodbye!"); 一般主程序中使用此退出.
        try:
            doulist_subject = soup.findAll('div', attrs={'class', 'doulist-subject'})
        except Exception as e:
            raise DropItem("details is null")

        items = []
        if doulist_subject:
            for listinfo in doulist_subject:
                item = DoubanItem()
                item['title'] = listinfo.find('div', attrs={'class', 'title'}).find('a').text.strip('\n')
                item['image'] = listinfo.find('div', attrs={'class', 'post'}).img['src']
                item['score'] = listinfo.find('span', attrs={'class', 'rating_nums'}).text

                strauthor = listinfo.find('div', attrs={'class', 'abstract'}).text
                authorinfo = strauthor.splitlines()
                authorinfo = [x.strip() for x in authorinfo if x.strip() != ""]
                item['author'] = authorinfo[0]
                item['publisher'] = authorinfo[1]
                item['publishdate'] = authorinfo[2]
                items.append(item)

        return items
