# -*- coding: utf-8 -*-
import urllib
import scrapy
from pick_a_university.items import UniversityScoreItem
from scrapy_splash import SplashRequest
import re


def update_dict(params_dict, key, value):
    params_dict.update({key: value})
    return params_dict


class UniversityScoreSpider(scrapy.spiders.Spider):
    name = 'university_score'
    allowed_domains = ['gkcx.eol.cn']
    params = {'page': 250, 'recomschtype': '普通本科', 'recomluqupici': '一批', 'scoreSign': 3, 'schoolSort': 7}
    base_url = 'http://gkcx.eol.cn/soudaxue/queryProvinceScore.html?%s'
    start_urls = [
        base_url % urllib.urlencode(params),
        base_url % urllib.urlencode(update_dict(params, 'page', 251)),
        base_url % urllib.urlencode(update_dict(params, 'page', 252)),
        base_url % urllib.urlencode(update_dict(params, 'page', 253)),
        base_url % urllib.urlencode(update_dict(params, 'page', 254)),
        base_url % urllib.urlencode(update_dict(params, 'page', 255))
    ]

    def start_requests(self):
        splash_args = {
            'wait': 0.5
        }
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.html',
                                args=splash_args)

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # tmp = response.css('.pageBox')
        # curr_page = tmp.xpath('.//a[contains(@style,"border")]/text()')[0].extract()
        curr_page = int(re.findall(r'page=\d+', response.url)[0][5:])
        tbody = response.xpath('//tbody')[0]
        for tr in tbody.xpath('.//tr'):
            if tr.re(r'queryProvinceScoreLeftad'):
                pass
            else:
                item = UniversityScoreItem()
                tds = tr.xpath('td/text()').extract()
                item['university'] = tr.xpath('.//td//a/text()')[0].extract()
                item['stu_src'] = tds[0]
                item['stu_type'] = tds[1]
                item['year'] = tds[2]
                item['grade_level'] = tds[3]
                item['avg_score'] = tds[4]
                item['score_line'] = tds[5]
                item['score_diff'] = tds[6]
                yield item
                print item['stu_src']

        if curr_page < 500:
            self.params['page'] = curr_page + 6
            url = self.base_url % urllib.urlencode(self.params)
            splash_args = {
                'wait': 0.5
            }
            yield SplashRequest(url, self.parse, endpoint='render.html',
                                args=splash_args)
