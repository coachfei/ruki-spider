import scrapy
import json
import datetime
import pprint


class GolukSpider(scrapy.Spider):
    name = "goluk"

    def start_requests(self):
        now = datetime.datetime.now()
        formats = "%Y%m%d%H%M%S%f"

        for i in range(30000):
            now = now - datetime.timedelta(hours=.5)
            url = 'https://s.goluk.cn/navidog4MeetTrans/shareVideo.htm?method=shareVideoSquare&xieyi=100&uid=&mobileid=99000774258247&channel=1&type=2&attribute=%5B%220%22%5D&operation=2&timestamp={}'.format(now.strftime(formats)[:-3])
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jsonresponse = json.loads(response.text)
        videos = jsonresponse["data"]["videolist"]
        for video in videos:
            yield {
                "id": video["video"]["videoid"],
                "location": video["video"]["location"],
                "path": video["video"]["ondemandwebaddress"],
            }
