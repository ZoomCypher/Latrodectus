from spiderGear.DataOutput import DataOutput
from spiderGear.HtmlDownloader import HtmlDownloader
from spiderGear.HtmlParser import HtmlParser
from spiderGear.UrlManager import UrlManager


class Schedule(object):

    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self, root_url):
        # add entrance url
        self.manager.add_new_url(root_url)
        while(self.manager.has_new_url() and self.manager.old_url_size()<100):
            try:
            # get new url from URLManager  
                new_url = self.manager.get_new_url()
                # downloader deal page content 
                html = self.downloader.download(new_url)
                # get new urls/url into URLmanager
                new_urls, data = self.parser.parser(new_url, html)
                # store file into database
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
                print "has crawled %s links" % self.manager.old_url_size() 
            except Exception, e:
                print e
                print "crawl filed"
            # store file with format
        self.output.output_html()
    
if __name__ == "__main__":
    schedule = Schedule()
    schedule.crawl("http://baike.baidu.com/view/284853.html")