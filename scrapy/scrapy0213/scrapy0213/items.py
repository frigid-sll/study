# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapy0213Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#爬虫获取到的数据组装成Item对象
class MovieItem(scrapy.Item):
    title = scrapy.Field()
    rank = scrapy.Field()
    subject = scrapy.Field()
    duration = scrapy.Field()