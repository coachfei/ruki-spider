import scrapy
import json


class DdpaiSpider(scrapy.Spider):
    name = "ddpai"

    def start_requests(self):
        for i in range(300000):
            url = 'http://app.ddpai.com/d/api/v1/storage/res/fragment/{}'.format(i);
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jsonresponse = json.loads(response.text)
        if jsonresponse["resobjs"][0]["type"] == 2:
            yield {
                "id": jsonresponse["id"],
                "des": jsonresponse["des"],
                "coords": [jsonresponse["longitude"], jsonresponse["latitude"]],
                "location": jsonresponse["location"],
                "path": jsonresponse["resobjs"][0]["remotePath"],
                "comments": jsonresponse["commentCount"],
                "views": jsonresponse["showViewedCount"],
                "likes": jsonresponse["favCount"],
                "type": jsonresponse["typeId"]
            }
