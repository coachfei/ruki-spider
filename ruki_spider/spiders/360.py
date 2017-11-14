import scrapy
import json


class GolukSpider(scrapy.Spider):
    name = "360"

    def start_requests(self):
        for i in range(720000, 1106000):
            url = 'http://wap.che.360.cn/share/h5/detail/{}'.format(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 视频ID
        id = response.url
        # 视频描述
        desc = "hello"
        # 视频路径
        param_values = response.css("#pc_player param::attr(value)")
        path = param_values[4].re(r"'url':'(.+)','autoPlay'") if len(param_values) != 0 else ""
        # 视频赞数
        likes = 1
        # 视频评论
        comments = 1
        yield {
            "path": path,
        }
