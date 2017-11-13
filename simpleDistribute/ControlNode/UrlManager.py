import cPickle
import hashlib

class UrlManager(object):
    def __init__(self):
        self.new_urls = self.load_progress('new_urls.txt') # uncrawled urls
        self.old_urls = self.load_progress('old_urls.txt') # crawled urls

    def has_new_urls(self):
        return self.new_url_size()!=0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        # set() will cause out of memory when url's link is long
        # use MD5 which is cutted out as 128bit 
        m = hashlib.md5()
        m.update(new_url)
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url
    
    def add_new_url(self, url):
        if url is None:
            return
        m = hashlib.md5()
        m.update(url)
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)
    
    def add_new_urls(self, urls):
        if urls is None or len(urls)==0:
            return 
        for url in urls:
            self.add_new_url(url)
    
    def new_url_size(self):
        return len(self.new_urls)

    def old_url_size(self):
        return len(self.old_urls)

    def save_progress(self, path, data):
        with open(path, 'wb') as f:
            cPickle.dump(data, f)
    
    def load_progress(self, path):
        print '[+] load processing from file: %s' % path
        try:
            with open(path, 'rb') as f:
                tmp = cPickle.load(f)
                return tmp
        except:
            print '[!] no processing file, create: %s' % path
        return set()