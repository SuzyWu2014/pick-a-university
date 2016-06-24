import scrapy
from pick_a_university.items import PickAUniversityItem


class ScoreLineSpider(scrapy.spiders.Spider):
    name = 'score_line'
    allowed_domains = ['gaokaopai.com']
    start_urls = [
        'http://www.gaokaopai.com/fenshuxian-sct-3-st-2-bt-1-year-2016.html',
        'http://www.gaokaopai.com/fenshuxian-sct-3-st-2-bt-1-year-2015.html',
        'http://www.gaokaopai.com/fenshuxian-sct-3-st-2-bt-1-year-2014.html',
        'http://www.gaokaopai.com/fenshuxian-sct-3-st-2-bt-1-year-2013.html',
        'http://www.gaokaopai.com/fenshuxian-sct-3-st-2-bt-1-year-2012.html',
        'http://www.gaokaopai.com/fenshuxian-sct-3-st-2-bt-1-year-2011.html',
        'http://www.gaokaopai.com/fenshuxian-sct-3-st-2-bt-1-year-2010.html'
    ]

    def parse(self, response):
        page_info = response.css('.pageInfo')[0].re(r'\d\/\d')[0].split('/')
        pages_count = int(page_info[1])
        curr_page = int(page_info[0])
        score_lines = response.selector.xpath('//table')[2]
        for line in score_lines.xpath('.//tr'):
            if line.re(r't1'):
                pass
            else:
                item = PickAUniversityItem()
                item['year'] = line.xpath('.//td/text()')[0].extract().encode('utf-8').strip()
                item['province'] = line.xpath('.//td/text()')[1].extract().encode('utf-8').strip()
                item['stu_type'] = line.xpath('.//td/text()')[2].extract().encode('utf-8').strip()
                item['grade_level'] = line.xpath('.//td/text()')[3].extract().encode('utf-8').strip()
                item['score_line'] = line.xpath('.//td/text()')[4].extract().encode('utf-8').strip()
                yield item
                print item['year'], item['province'], item['stu_type'], item['grade_level'], item['score_line']
        if curr_page < pages_count:
            url = 'http://www.gaokaopai.com/fenshuxian-sct-3-st-2-bt-1-year-2016-p-%s.html' % str(curr_page + 1)
            yield scrapy.Request(url, callback=self.parse)
