# -*- coding: utf-8 -*-
import urllib
import scrapy
from major_score_spider.items import MajorScoreSpiderItem
from scrapy_splash import SplashRequest
import re


def update_dict(params_dict, key, value):
    params_dict.update({key: value})
    return params_dict


class Score2011Spider(scrapy.spiders.Spider):
    name = 'score_2011'
    allowed_domains = ['gkcx.eol.cn']
    params = {'page': 1, 'recomschtype': '普通本科', 'recomluqupici': '一批', 'scoreSign': 3, 'schoolSort': 4, 'recomyear': 2011, 'argprovince': '福建', 'argluqutype': '理科'}
    base_url = 'http://gkcx.eol.cn/soudaxue/querySpecialtyScore.html?%s'
    start_urls = [base_url % urllib.urlencode(params)]

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
        curr_page = int(re.findall(r'page=\d+', response.url)[0][5:])
        # with open("url.txt", 'wb') as f:
        #     f.write(str(curr_page))
        #     f.write('\n')
        tbody = response.xpath('//tbody')
        if len(tbody) > 0:
            tbody = tbody[0]
            for tr in tbody.xpath('.//tr'):
                if tr.re(r'querySpecialtyScoreLeftad'):
                    pass
                else:
                    # print tr.extract()
                    item = MajorScoreSpiderItem()
                    tds = tr.xpath('td/text()').extract()
                    item['university'] = tr.xpath('.//td//a/text()')[0].extract()
                    item['major'] = tds[0]
                    item['year'] = tds[3]
                    item['avg_score'] = tds[5]
                    yield item
                    print item['university']
                    # print tds[0], tds[1], tds[2], tds[3], tds[4], tds[5]
        else:
            yield SplashRequest(response.url, self.parse, endpoint='render.html',
                                args={'wait': 0.5})
        if curr_page < 349:
            self.params['page'] = curr_page + 1
            url = self.base_url % urllib.urlencode(self.params)
            splash_args = {
                'wait': 0.5
            }
            yield SplashRequest(url, self.parse, endpoint='render.html',
                                args=splash_args)
