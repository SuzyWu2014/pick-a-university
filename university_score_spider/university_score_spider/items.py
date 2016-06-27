# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class UniversityScoreSpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    university = Field()
    year = Field()
    avg_score = Field()
    score_line = Field()
    score_diff = Field()
