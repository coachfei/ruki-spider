#! /usr/bin/env python
# coding=utf-8
# MIT License
#
# Copyright (c) 2017 Zeu Fung
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click
import json
import os
from tqdm import tqdm
import requests
import time
from datetime import datetime
from shutil import copyfile

# 版本号和名字
APP_NAME = "ruki_ddpai"
APP_VERSION = "0.01"


def merge_items(old_name, new_name):
    # 备份就结果
    bak_name = "tmp/{}.json".format(datetime.now().strftime("%Y%m%d"))
    copyfile(old_name, bak_name)
    # 将旧结果和新结果合并
    with open(old_name, "r") as old_file:
        old_items = json.load(old_file)
        with open(new_name, "r") as new_file:
            new_items = json.load(new_file)
            not_found_total = 0
            for new_item in new_items:
                is_found = False
                for old_item in old_items:
                    if old_item["id"] == new_item["id"]:
                        is_found = True
                        break
                if not is_found:
                    old_items.append(new_item)
                    not_found_total = not_found_total + 1
                    print("index not found: {}".format(new_item["id"]))
                else:
                    print("index found: {}".format(new_item["id"]))
            print("index not found sum: {}".format(not_found_total))
    # 覆盖旧结果
    with open(old_name, "w") as old_file:
        print("dumping {} items into {}".format(len(old_items), old_name))
        json.dump(old_items, old_file)

def generate_index(old_name):
    ret = {}
    # 根据数据文件分拣索引文件， ddpai.jsons是scrapy的文件，数组，元素是视频信息
    with open(old_name, "r") as data_file:
        items = json.load(data_file)
        for i, item in enumerate(items):
            typeId = item["type"]
            comments = item["comments"]
            likes = item["likes"]
            itemId = item.pop("id", None)
            key = "t{}_c{}_l{}".format(typeId, 1 if comments > 0 else 0, 1 if likes > 0 else 0)
            item.update({"i": i})
            if key in ret:
                ret[key].update({itemId: item})
            else:
                ret.update({key: {itemId: item}})
    return ret


def save_index(item_dict):
    #保存索引文件到文件夹下
    for key, group in item_dict.items():
        # 检查文件夹路径
        folder = "ddpai_{}".format(key)
        filepath = "{}/index.json".format(folder)
        if not os.path.exists(folder):
            os.mkdir(folder)
        if os.path.exists(filepath):
            os.remove(filepath)
        # 复制索引文件
        with open(filepath, "w") as out_file:
            print("saving index file contains {} items into {}".format(len(group), filepath))
            json.dump(group, out_file)


def download_video(from_path, to_path):
    # 下载媒体文件
    r = requests.get(from_path, stream=True, timeout=10)
    with open(to_path, "wb") as f:
        totalSize = int(r.headers.get("content-length", 0))
        chunkSize = 32*1024
        pbar = tqdm(total=totalSize, unit="B", unit_scale=True)
        for chunk in r.iter_content(chunkSize):
            pbar.update(len(chunk))
            f.write(chunk)


def generate_videos(item_dict):
    # 遍历文件夹下载媒体文件
    for key, group in item_dict.items():
        total = len(group)
        folder = "ddpai_{}".format(key)
        for i, (itemId, item) in enumerate(group.items()):
            remote_src = item["path"]
            des_src = "{}/{}.mp4".format(folder, itemId)
            if not os.path.exists(des_src):
                print("[{}][{}/{}] downloading {} to {}".format(datetime.now(), i, total, remote_src, des_src))
                download_video(remote_src, des_src)
            else:
                print("[{}][{}/{}] {} already exists".format(datetime.now(),i, total, des_src))


def count_videos(item_dict):
    # 统计文件夹下的媒体文件
    all_count = 0
    all_total = 0
    for key, group in item_dict.items():
        # 检查文件夹路径
        folder = "ddpai_{}".format(key)
        if not os.path.exists(folder):
            print("folder {} does not exists".format(folder))
            continue
        count = 0
        total = len(group)
        all_total = all_total + total
        for i, (itemId, item) in enumerate(group.items()):
            des_src = "{}/{}.mp4".format(folder, itemId)
            if os.path.exists(des_src):
                count = count + 1
                all_count = all_count + 1
        print("{} {}: {}/{}".format("*" if count == total else "!", folder, count, total))

    print("summary: {}/{}".format(all_count, all_total))


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("{} v{}".format(APP_NAME, APP_VERSION))
    ctx.exit()


@click.group()
@click.option("--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option("--debug", is_flag=True, default=False)
def cli(debug):
    if debug:
        print("Debug mode is on")
    pass


@cli.command(help="generate videos for each folder")
@click.option("-o", help="old result")
def generate(o):
    if os.path.exists(o):
        # 生成索引字典，键是“t类型ID_c评论数_l喜欢数”，值是视频信息
        item_dict = generate_index(o)
        # 保存索引文件
        save_index(item_dict)
        # 根据索引文件，循环执行下载视频
        while True:
            try:
                generate_videos(item_dict)
            except:
                pass
            time.sleep(15)
    else:
        print("result file not exist")


@cli.command(help="count videos for each folder")
@click.option("-o", help="old result")
def count(o):
    if os.path.exists(o):
        # 生成索引字典，键是“t类型ID_c评论数_l喜欢数”，值是视频信息
        item_dict = generate_index(o)
        # 统计媒体文件
        count_videos(item_dict)
    else:
        print("result file not exist")


@cli.command(help="merge new result into old result")
@click.option("-o", help="old result")
@click.option("-n", help="new result")
def merge(o, n):
    if os.path.exists(o) or os.path.exists(n):
        # 合并结果集合
        merge_items(o, n)
    else:
        print("result files not exist")


@cli.command(help="test new command")
def test():
    ret = datetime.now().strftime("%Y%m%d")
    print(ret)


if __name__ == "__main__":
    cli()
