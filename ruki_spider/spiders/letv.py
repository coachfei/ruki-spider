import scrapy
import json
from selenium import webdriver
import sys

class GolukSpider(scrapy.Spider):
    name = "letv"

    def __init__(self):
        self.driver = webdriver.Firefox()

    def start_requests(self):
        url = 'http://camera.leautolink.com/share/share.jsp?id=72790'
        yield scrapy.Request(url=url, callback=self.parse)
        # for i in range(1106000):
        #     url = 'http://wap.che.360.cn/share/h5/detail/{}'.format(i)
        #     yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        self.driver.get(response.url)

        while True:
            next = self.driver.find_element_by_id('player_img')
            try:
                # self.driver.implicitly_wait(1)
                # next.click()
                path = response.css("#player_img").extract_first()
                print(path)
                # yield {
                #     "path": path,
                # }
            except:
                e = sys.exc_info()[0]
                print(e)
                break

        self.driver.close()
