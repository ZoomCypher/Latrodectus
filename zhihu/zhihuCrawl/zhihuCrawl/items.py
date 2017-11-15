# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
import scrapy

class ZhihucrawlItem(scrapy.Item):

    user_id = Field()
    user_image_url = Field()
    name = Field()
    location = Field()
    business = Field()
    gender = Field()
    employment = Field()
    position = Field()
    education = Field()
    followees_num = Field()
    followers_num = Field()


class RelationItem(scrapy.Item):
    
    user_id = scrapy.Field()
    relation_type = scrapy.Field()
    relations_id = scrapy.Field()
    
