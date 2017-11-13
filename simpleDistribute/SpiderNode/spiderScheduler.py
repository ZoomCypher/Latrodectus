from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParser
from multiprocessing.managers import BaseManager


class SpiderWork(object):
    
    def __init__(self):
        """
        initialization:
            1. initial distribution process then connect to control node
            2. register basemanager for get Queue
            3. sync with control node 
        """
        # 1. register
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        # 2. connect to server
        server_addr = '127.0.0.1'
        print "connect to server %s..." % server_addr
        # 3. match port & authkey with control node
        self.m = BaseManager(address=(server_addr, 8001), authkey='baike')
        self.m.connect()
        # 4. get Queue object (url_q, result_q)
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        # 5. initialize downloader, parser
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        print 'init finish'

    def crawl(self):
        while(True):
            try:
                if not self.task.empty():
                    url = self.task.get()

                    if url == 'end':
                        print 'control node inform spider node stop working'
                        self.result.put({'new_urls':'end', 'data':'end'})
                        return
                    print 'spider node is parsing:%s' % url.encode('utf-8')
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content)
                    self.result.put({"new_urls":new_urls, "data":data})
            except EOFError, e:
                print "work node connect filed"
                return 
            except Exception, e:
                print e
                print 'Crawl fail'

if __name__ == "__main__":
    spider = SpiderWork()
    spider.crawl()