# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import codecs
# from scrapy.contrib.exporter import JsonLinesItemExporter


class StuSrcPipiline(object):
    """docstring for StuSrcPipiline"""

    def process_item(self, item, spider):
        if item['stu_src'] == u"福建":
            return item
        else:
            raise DropItem("Not for Students from Fujian!")


class ScoreDiffPipeline(object):

    def process_item(self, item, spider):
        score_diff = int(item['score_diff'])
        if score_diff > 50 and score_diff < 120:
            return item
        else:
            raise DropItem("score_diff not matched!")


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('university_cores.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
