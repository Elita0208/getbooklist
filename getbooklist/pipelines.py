# -*- coding: utf-8 -*-
from scrapy.conf import settings
import pymongo
import MySQLdb
from datetime import date, datetime
from scrapy.exceptions import DropItem
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GetbooklistPipeline(object):
    def process_item(self, item, spider):
        item['spider'] = spider.name
        return item

class MongoClient(object):
    server = settings['MONGODB_SERVER']
    port = settings['MONGODB_PORT']
    db = settings['MONGODB_DB']

    def __init__(self):
        self.connection = pymongo.MongoClient(MongoClient.server, MongoClient.port)
        self.db = self.connection[MongoClient.db]

class MongoDoubanPipeline(MongoClient):
    def __init__(self):
        super(MongoDoubanPipeline,self).__init__()
        self.col = 'douban_list'
        self.collection = self.db[self.col]

    def process_item(self, item, spider):
        if spider.name in ['Douban']:
            book = self.collection.find_one({'title': item["title"]})
            self.collection.update({'title': item["title"]}, {'$set': dict(item)}, upsert=True)
        return item
