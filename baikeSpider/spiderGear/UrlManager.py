class UrlManager(object):
    def __init__(self):
        self.new_urls = set() # uncrawled URLs
        self.old_urls = set() # crawled URLs
    
    def has_new_url(self):
        """
        check uncrawled url
        """
        return self.new_url_size()!=0

    def get_new_url(self):
        """
        get a uncrawled url
        """
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        """
        add uncrawled url into uncrawled URLs connections
        """
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)
        
    def add_new_urls(self, urls):
        """
        add a group uncrawled urls into uncrawled URLS connections
        """
        if urls is None or len(urls)==0:
            return 
        for url in urls:
            self.add_new_url(url)
    
    def new_url_size(self):
        """
        get the length of uncrawled URLs connection
        """
        return len(self.new_urls)
    
    def old_url_size(self):
        """
        get the length of crawled URLs connection
        """
        return len(self.old_urls)
