# -*- coding: utf-8 -*-
import scrapy
from quotetutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # pass
        # pass 默认回调方法
        # print("response.text")
        quotes = response.css('.quote')
        for quote in quotes:
            item=QuoteItem()
            #在items.py中定义的
            text = quote.css('.text::text').extract_first()
            #进一步筛选quote
            #::是特有的语法结构，是输出text中文本
            #extract_first找第一个结果
            author = quote.css('.author::text').extract_first()
            tags = quote.css('.tags .tag::text').extract()
            #tag有多个，extract提取全部内容，类似于find(),findall()
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item
        #下一页提取
        next = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next)
        #urljon()生成一个网站的url
        yield scrapy.Request(url=url,callback=self.parse)
        #回调自己，翻页




