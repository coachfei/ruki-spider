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
import os
import time

# 版本号和名字
APP_NAME = "ruki_spider"
APP_VERSION = "0.01"

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


@cli.command(help="ddpai")
@click.option("--crawl", is_flag=True, default=False)
@click.option("--download", is_flag=True, default=False)
def ddpai(crawl, download):
    if crawl:
        while True:
            try:
                os.remove("ddpai/tmp/new.json")
                os.system("scrapy crawl ddpai -o ddpai/tmp/new.json")
                os.system("python3 ddpai/ddpai.py merge -o ddpai/tmp/ddpai.json -n ddpai/tmp/new.json")
            except:
                pass
            time.sleep(15)
    if download:
        os.system("python3 ddpai/ddpai.py generate -o ddpai/tmp/ddpai.json")


@cli.command(help="s360 spider")
@click.option("--crawl", is_flag=True, default=False)
@click.option("--download", is_flag=True, default=False)
def s360(crawl, download):
    if crawl:
        while True:
            try:
                os.remove("s360/tmp/new.json")
                os.system("scrapy crawl s360 -o s360/tmp/new.json")
                os.system("python3 s360/s360.py merge -o s360/tmp/s360.json -n s360/tmp/new.json")
            except:
                pass
            time.sleep(15)
    if download:
        os.system("python3 s360/s360.py generate -o s360/tmp/s360.json")


if __name__ == "__main__":
    cli()
