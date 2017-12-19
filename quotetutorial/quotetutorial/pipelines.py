# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

############################################
####如果保存的时候，我们要挑选item，或者保存如数据库，tutoria就不行了，
####要换成xxx工具
# class QuotetutorialPipeline(object):
#     def process_item(self, item, spider):
#         return item
############################################
from scrapy.exceptions import DropItem
import pymongo



# 如果名言太长，就要阶段，在增加一个省略号
class TextPipeline(object):
    def __init__(self):
        self.limit=50
    def process_item(self, item, spider):
        # return item
        if item['text']:
            if len(item['text'])>self.limit:
                item['text']=item['text'][0:self.limit].rstrip()+'...'
            return item
        else:
            return DropItem('Missing Text')

class MongoPipeline(object):
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url=mongo_url
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):
    # from_crawler()从settings里面拿到配置信息,初始化
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
     #爬虫刚启动的时候，要做的工作
        self.client=pymongo.MongoClient(self.mongo_url)
        self.db=self.client[self.mongo_db]
    def process_item(self,item,spider):
         name = item.__class__.__name__
         self.db['quotes'].insert(dict(item))
         return item

    def close_spider(self,spider):
         self.client.close()
