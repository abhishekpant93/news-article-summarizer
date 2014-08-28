import scrapy
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from nytimes_scraper.items import NytimesItem
from time import sleep
import re

class NytimesSpider(CrawlSpider):
    name = "nytimes"
    allowed_domains = ["nytimes.com"]
    start_urls = [
        "http://www.nytimes.com/"
    ]

    def filter_unicode(self, str):
        str = str.replace("u'", "")
        str = str.replace("\u201d","\"")
        str = str.replace("\u201c", "\"")
        str = str.replace("\u2019", "'")
        str = str.replace("\u2018", "'")
        str = str.replace("\u2014", " ")
        str = str.replace("\'", "")
        str = str.replace("\"", "")
        return str
        
    def parse(self, response):
        item = NytimesItem()
        item['headline'] = self.filter_unicode(str(response.xpath("//meta[@property='og:title']/@content").extract())[1:-1])
        item['link'] = response.url
        text = ""
        i = 0
        num_pars = len(response.xpath('//*[@class="story-body-text story-content"]'))

        while i < num_pars:
            par = str(response.xpath(('//*[@id="story"]/p[%d]/text()') % i).extract())[1:-1]
            # print 'par_orig: ' + par
            par = self.filter_unicode(par)
            # print 'par_processed: ' + par
            text += par
            i += 1
            
        item['text'] = text
        item['keywords'] = self.filter_unicode(str(response.xpath("//meta[@name='news_keywords']/@content").extract())[1:-1])

        yield item

        for url in response.xpath('//a/@href').extract():
            if re.match(r'http://www.nytimes.com/2014.*\.html', url):
                print 'match. yielding new req: ' + url
                yield scrapy.Request(url, callback=self.parse)

        sleep(0.5)
        
