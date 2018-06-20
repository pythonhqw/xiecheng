# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiechengItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    city_name = scrapy.Field()
    city_link = scrapy.Field()
    city_id = scrapy.Field()
    hotel_name = scrapy.Field()
    hotel_zone = scrapy.Field()
    hotel_score = scrapy.Field()
    hotel_price = scrapy.Field()
    hotel_link = scrapy.Field()

