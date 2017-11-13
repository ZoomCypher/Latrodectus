import requests

class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None
        user_agent = "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )"
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding='utf-8'
            return response.text
        return None
