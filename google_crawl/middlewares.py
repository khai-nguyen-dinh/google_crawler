import os
import random

from proxylist import ProxyList

from google_crawl.settings import BASE_DIR


class ProxyMiddleware(object):
    def __init__(self):
        self.pl = ProxyList()
        self.pl.load_file(os.path.join(BASE_DIR, 'proxy/proxy-list.txt'))

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://{}'.format(self.pl.random().address())

class RandomUserAgentMiddleware(object):
    def __init__(self):
        super(RandomUserAgentMiddleware, self).__init__()
        self.uas = []
        with open('google_crawl/source/user_agents.txt', 'r') as sites:
            for site in sites:
                self.uas.append(site)

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.uas[random.randint(0, len(self.uas) -1)])