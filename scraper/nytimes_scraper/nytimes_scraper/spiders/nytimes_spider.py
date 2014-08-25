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
               
    def parse(self, response):
        item = NytimesItem()
        item['headline'] = str(response.xpath("//meta[@property='og:title']/@content").extract())
        item['link'] = response.url
        text = ""
        i = 0
        num_pars = len(response.xpath('//*[@class="story-body-text story-content"]'))
        while i < num_pars:
            text += str(response.xpath(('//*[@id="story"]/p[%d]/text()') % i).extract())
            #print 'par: ' + text
            i += 1
        item['text'] = text
        item['keywords'] = str(response.xpath("//meta[@name='news_keywords']/@content").extract())

        yield item

        for url in response.xpath('//a/@href').extract():
            if re.match(r'http://www.nytimes.com/2014.*\.html', url):
                print 'match. yielding new req: ' + url
                yield scrapy.Request(url, callback=self.parse)

        sleep(0.5)
