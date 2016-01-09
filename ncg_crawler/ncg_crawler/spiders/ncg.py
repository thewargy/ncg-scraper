# -*- coding: utf-8 -*-
import scrapy
import re
from ncg_crawler.items import NcgCrawlerItem

class NcgSpider(scrapy.Spider):
    name = "ncg"
    # EDIT YOUR NCG USERNAME AND PASSWORD HERE
    self.username = username
    self.password = password
    allowed_domains = ["netcodeguides.com"]
    start_urls = (
        'http://www.netcodeguides.com/login',
    )
    def parse(self, response):
        return [scrapy.FormRequest.from_response(response,
            formdata={'username': self.username, 'password': self.password},
            callback=self.after_login)]


    def after_login(self, response):
        #print response.body

        if "You have Netcode Premium!" in response.body:
            print "LOGIN SUCCESS!"
            request_list = []
            for page in range(26,76):
                url="http://www.netcodeguides.com/videos?p={page}".format(page=page)
                request_list.append(scrapy.Request(url=url, callback=self.parse_videos))
            return request_list
        else:
            return

    def parse_videos(self, response):
        hxs = scrapy.Selector(response)
        media_headings = hxs.xpath("//div[@class='panel panel-netcode'][2]//h4[@class='media-heading']")
        for heading in media_headings:
            link = heading.xpath("a/@href").extract()
            url = ''.join(('http://www.netcodeguides.com', link[0]))
            yield scrapy.Request(url, callback=self.parse_watch_contents)
        pass

    def parse_watch_contents(self, response):
        item = NcgCrawlerItem()
        title = response.xpath("//div[@class='panel-heading']/h3/text()").extract()
        item['title'] = title[0]
        for iframe in response.xpath("//div[@class='media']/iframe"):
            link = iframe.xpath("@src").extract()
            m = re.search('//player.vimeo.com/video/([0-9]+)', link[0])
            if m:
                item['link'] = m.group(1)
            return item
