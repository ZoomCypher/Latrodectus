# -*- coding: utf-8 -*-
import json, re
import os
from urllib import urlencode

import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from zhihuCrawl.items import UserInfoItem, RelationItem
from scrapy.http import Request, FormRequest


class ZhihuspiderSpider(CrawlSpider):
    name = 'zhihuSpider'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    def __init__(self, *args, **kwargs):
        super(ZhihuspiderSpider, self).__init__(*args, **kwargs)
        self.xsrf = ''
        self.cookies = ''
        
    def start_requests(self):

        return [Request(
              'https://www.zhihu.com/#signin',
               callback = self.start_login,
               meta = {'cookiejar': 1}
            )]

    def start_login(self, response):
        self.xsrf = Selector(response).xpath(
                '//input[@name="_xsrf"]/@value'
                ).extract_first()

        return [FormRequest(
              'https://www.zhihu.com/login/phone_num',
               method = 'POST',
               meta = {'cookiekar': response.meta['cookiekar']},
               formdata = {
                   '_xsrf': self.xsrf,
                   'phone_num': 'xxxxxx',
                   'password': 'xxxxxx',
                   'captcha_type': 'cn'
                   },
               callback = self.after_login
            )]

    def after_login(self, response):
        if json.loads(response.body)['msg'].encode('utf8') == "login successful":
            self.logger.info(str(response.meta['cookiejar']))

            return [Request(
                   self.start_urls[0],
                   meta = {'cookiekar': response.meta['cookiejar']},
                   callback = self.parse_url_info,
                   errback = self.parse_err,
                )]
        else:
            self.logger('login failed')
            return
        
    def parse_user_info(self, response):
        """
        functions:
           1. parse user info
           2. parse relation info
        """
        user_id = os.path.split(response.url)[-1]
        user_image_url = response.xpath("").extract_first()
        name = response.xpath("").extract_first()
        location = response.xpath("").extract_first()
        business = response.xpath("").extract_first()
        gender = response.xpath("").extract_first()
        if gender and u'female' in gender:
            gender = u'female'
        else:
            gender = u'male'
        employment = response.xpath("").extract_first()
        position = response.xpath("").extract_first()
        education = response.xpath("").extract_first()

        try:
            followee_num, followers_num = tuple(response.xpatj("").extract())
            relations_url = response.xpath("").extract()
        except Exception, e:
            followee_num, followers_num = tuple(response.xpatj("").extract())
            relations_url = response.xpath("").extract()

        user_info_item = UserInfoItem(
                 user_id = user_id,
                 user_image_url = user_image_url,
                 name = name,
                 location = location,
                 business = business,
                 gender = gender,
                 employment = employement,
                 position = position,
                 education = education,
                 followees_num = int(followees_num)
                 followers_num = int(followers_num)
                )

        yield user_info_item




             
             







