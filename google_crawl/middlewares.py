import os
import random

from google_crawl.settings import BASE_DIR
from proxylist import ProxyList


class ProxyMiddleware(object):
    def __init__(self):
        self.pl = ProxyList()
        self.index = 0
        self.pl.load_file(os.path.join(BASE_DIR, 'proxy/proxy-list.txt'))

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://{}'.format(self.pl[self.index].address())
        print self.pl[self.index]
        self.index = (self.index + 1) % self.pl.size()



# class RandomUserAgentMiddleware(object):
#     def __init__(self):
#         super(RandomUserAgentMiddleware, self).__init__()
#
#         self.uas = []
#
#         with open(os.path.join(BASE_DIR, 'source/user_agents.txt')) as agents:
#             for agent in agents:
#                 self.uas.append(agent.strip())
#
#     def process_request(self, request, spider):
#         request.headers.setdefault('User-Agent', random.choice(self.uas))
