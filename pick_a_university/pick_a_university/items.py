# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PickAUniversityItem(Item):
    # define the fields for your item here like:
    province = Field()
    year = Field()
    stu_type = Field()
    grade_level = Field()
    score_line = Field()
