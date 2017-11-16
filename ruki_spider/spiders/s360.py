import scrapy
import json
import re


class S360Spider(scrapy.Spider):
    name = "s360"

    def start_requests(self):
        # for i in range(1336300, 1336400):
        for i in range(1336400):
            url = 'http://wap.che.360.cn/share/h5/detail/{}'.format(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 视频ID
        m = re.match(r"^http://wap.che.360.cn/share/h5/detail/(\d+)$", response.url)
        if m is None:
            return
        item_id = m.group(1)
        # 视频路径
        path_doms = response.css("#pc_player param::attr(value)")
        if len(path_doms) < 5:
            return
        path_vals = path_doms[4].re(r"'url':'(.+)','autoPlay'")
        if not path_vals:
            return
        path = path_vals[0]
        # 视频描述
        des_vals = response.css("div.share-panel p::text").extract()
        des = des_vals[0] if len(des_vals) == 1 else ""
        # 视频赞数
        likes_vals = response.css("div.likes-inner div::text").re(r"^(\d+)个赞$")
        likes = likes_vals[0] if len(likes_vals) == 1 else 0
        # 视频评论
        comments_vals = response.css("#comment-tab-btn::text").re(r"^评论\((\d+)\)")
        comments = comments_vals[0] if len(comments_vals) == 1 else 0
        yield {
            "id": item_id,
            "path": path,
            "des": des,
            "path": path,
            "comments": comments,
            "likes": likes
        }
