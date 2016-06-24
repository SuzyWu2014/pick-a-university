import scrapy
from pick_a_university.items import ScoreLineItem


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
        curr_year = "2016"
        with open("score_line.txt", 'a') as f:
            for line in score_lines.xpath('.//tr'):
                if line.re(r't1'):
                    year = line.xpath('.//th/text()')[0].extract().encode('utf-8').strip()
                    province = line.xpath('.//th/text()')[1].extract().encode('utf-8').strip()
                    stu_type = line.xpath('.//th/text()')[2].extract().encode('utf-8').strip()
                    grade_level = line.xpath('.//th/text()')[3].extract().encode('utf-8').strip()
                    score_line = line.xpath('.//th/text()')[4].extract().encode('utf-8').strip()
                    table_head = "%s\t%s\t%s\t%s\t%s\n" % (year, province, stu_type, grade_level, score_line)
                    f.write(table_head)
                else:
                    item = ScoreLineItem()
                    curr_year = item['year'] = line.xpath('.//td/text()')[0].extract().encode('utf-8').strip()
                    item['province'] = line.xpath('.//td/text()')[1].extract().encode('utf-8').strip()
                    item['stu_type'] = line.xpath('.//td/text()')[2].extract().encode('utf-8').strip()
                    item['grade_level'] = line.xpath('.//td/text()')[3].extract().encode('utf-8').strip()
                    item['score_line'] = line.xpath('.//td/text()')[4].extract().encode('utf-8').strip()
                    yield item
                    item_str = "%s\t%s\t\t%s\t\t%s\t\t%s\n" % (item['year'], item['province'], item['stu_type'], item['grade_level'], item['score_line'])
                    f.write(item_str)
        # f.close()
        if curr_page < pages_count:
            url = 'http://www.gaokaopai.com/fenshuxian-sct-3-st-2-bt-1-year-%s-p-%s.html' % (curr_year, str(curr_page + 1))
            yield scrapy.Request(url, callback=self.parse)


class UniversityScoreSpider(scrapy.spiders.Spider):
    name = 'university_score'
    allowed_domains = ['gkcx.eol.cn']
    start_urls = ['http://gkcx.eol.cn/soudaxue/queryProvinceScore.html?page=1&recomschtype=%E6%99%AE%E9%80%9A%E6%9C%AC%E7%A7%91&recomluqupici=%E4%B8%80%E6%89%B9&scoreSign=3&schoolSort=7']

    def parse(self, response):
        pass
