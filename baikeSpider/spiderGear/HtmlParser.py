import re 
import urlparse
from bs4 import BeautifulSoup

class HtmlParser(object):

    def parser(self, page_url, html_cont):
        """
        analyse the page content, and catch the
        urls and data
        """
        if page_url is None or html_cont is None:
            return 
        soup = BeautifulSoup(html_cont, 'html.parser',from_encoding='utf-8')
        new_urls = self.__get_new_urls(page_url, soup)
        new_data = self.__get_new_data(page_url, soup)
        return new_urls, new_data

    def __get_new_urls(self, page_url, soup):
        """
        get and download uncrawled URLs collection
        """
        new_urls = set()
        links = soup.find_all('a', href = re.compile(r'/item/.*'))
        for link in links:
            # get element
            new_url = link['href']
            # complete a url
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def __get_new_data(self, page_url, soup):
        """
        get valid data
        """
        data = {}
        data['url'] = page_url
        title = soup.find('dd', class_ = 'lemmaWgt-lemmaTitle-title').find('h1')
        data['title'] = title.get_text()
        summary = soup.find('div', class_= 'lemma-summary')  
        # fetch tag# contents include their kids' contents
        # and return its as a unicode string 
        data['summary'] = summary.get_text()
        return data


