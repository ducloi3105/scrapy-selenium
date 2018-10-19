# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PhysioItem(scrapy.Item):
    # define the fields for your item here like:
    practitioner_name = scrapy.Field()
    practise_name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field(serializer=str)
    fax = scrapy.Field(serializer=str)
    email = scrapy.Field()
    web_url = scrapy.Field()
    profile_url = scrapy.Field()
    postcode_searched = scrapy.Field()
