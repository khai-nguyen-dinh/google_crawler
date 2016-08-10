import os

import scrapy
from google_crawl.items import GoogleCrawlItem
from google_crawl.settings import BASE_DIR


class Google(scrapy.Spider):
    name = 'google'
    allowed_domains = ['http://google.com/']
    start_urls = []
    except_sites = ''

    with open(os.path.join(BASE_DIR, 'source/site_except.txt')) as sites:
        for site in sites:
            except_sites = '{}+{}'.format(except_sites, site.strip())

    with open(os.path.join(BASE_DIR, 'source/categories.txt')) as category:
        for cate in category:
            with open(os.path.join(BASE_DIR, 'source/countries.txt')) as countries:
                for country in countries:
                    query = '{} company {}'.format(cate.strip(), country.strip())
                    url = 'https://www.google.com/search?q={}'.format(query.replace(' ', '+'))
                    start_urls.append(url)

    def parse(self, response):
        for sel in response.xpath('//div[@class="g"]'):
            temp = GoogleCrawlItem()
            url = sel.xpath('div[@class="rc"]/h3/a/@href').extract_first()
            temp['url'] = url.split('/')[2]
            temp['title'] = sel.xpath('div[@class="rc"]/h3/a/text()').extract_first()
            temp['content'] = sel.xpath('string(div[@class="rc"]/div[@class="s"]/div/span)').extract_first()
            yield temp
