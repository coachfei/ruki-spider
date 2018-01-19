# ruki-spider
路几爬虫，爬取原始信息并分类到特定文件夹

## 依赖
* Python 3.5或以上版本
* Scrapy 1.4或以上版本

## 使用方法
### DDPAI
#### 爬取数据
从目标网站爬取索引信息并保存 `scrapy crawl ddpai -o ddpai/tmp/new.json`
#### 合并数据
刚爬取的索引信息合并到旧索引 `python3 ddpai/ddpai.py merge -o ddpai/tmp/ddpai.json -n ddpai/tmp/new.json`
#### 下载媒体
根据索引分类媒体文件并下载到相应文件夹 `python3 ddpai/ddpai.py generate -o ddpai/tmp/ddpai.json`
#### 统计媒体
根据索引统计媒体下载数目 `python3 ddpai/ddpai.py count -o ddpai/tmp/ddpai.json`

### 360
#### 爬取数据
从目标网站爬取索引信息并保存 `scrapy crawl s360 -o s360/tmp/new.json`
#### 合并数据
刚爬取的索引信息合并到旧索引 `python3 s360/s360.py merge -o s360/tmp/s360.json -n s360/tmp/new.json`
#### 下载媒体
根据索引分类媒体文件并下载到相应文件夹 `python3 s360/s360.py generate -o s360/tmp/s360.json`
#### 统计媒体
根据索引统计媒体下载数目 `python3 s360/s360.py count -o s360/tmp/s360.json`

### GOLUK
#### 爬取数据
从目标网站爬取索引信息并保存 `scrapy crawl goluk -o goluk/tmp/new.json`

### LETV
#### 未完成

### YI
#### 未完成
