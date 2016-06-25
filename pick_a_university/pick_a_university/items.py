# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ScoreLineItem(Item):
    # define the fields for your item here like:
    province = Field()
    year = Field()
    stu_type = Field()
    grade_level = Field()
    score_line = Field()


class UniversityScoreItem(Item):
    """
    university: Unversity Name
    stu_src:
    stu_type:
    year:
    grade_level:
    avg_score:
    score_line:
    score_diff:
    """
    university = Field()
    stu_src = Field()
    stu_type = Field()
    year = Field()
    grade_level = Field()
    avg_score = Field()
    score_line = Field()
    score_diff = Field()
