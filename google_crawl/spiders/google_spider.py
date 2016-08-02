import json
import scrapy
from bs4 import BeautifulSoup

from google_crawl.items import GoogleCrawlItem


class Stackover(scrapy.Spider):
    name = 'google'
    allowed_domains = ['http://google.com/']
    start_urls = []
    except_sites = ''

    with open('google_crawl/source/site_except.txt','r') as sites:
        for site in sites:
            except_sites = except_sites + '+' + site.strip('\n')

    with open('google_crawl/source/categories.txt', 'r') as category:
        for cate in category:
            with open('google_crawl/source/countries.txt', 'r') as country:
                for count in country:
                    text = cate + ' company' + ' ' + count
                    url = 'http://www.google.com/search?q=' + text.replace(' ', '+') + except_sites
                    start_urls.append(url)

    def parse(self, response):
        for rel in response.xpath('//div[@class="g"]'):
            temp = GoogleCrawlItem()
            url = response.xpath('//div[@class="g"]/div[@class="rc"]/h3/a/@href').extract_first()
            temp['url'] = url.split('/')[2]
            temp['title'] = response.xpath('//div[@class="g"]/div[@class="rc"]/h3/a/text()').extract_first()
            temp['content'] = response.xpath('string(//div[@class="g"]/div[@class="rc"]/div[@class="s"]/div/span)').extract_first()
            yield temp



