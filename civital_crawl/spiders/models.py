import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from civital_crawl.items import *
import json
import os
import re
import numpy as np

def get_all_items(path, num:int):
    ls = list()
    for i in range(1, num+1):
        with open(os.path.join(path, f"{i}.json"), "r") as f:
            dic = json.loads(f.read())
            ls += dic["items"]
    return ls


class CiviModelSpider(scrapy.Spider):
    name = "civi_meta"
    allowed_domains = ["civitai.com"]
    data_base = "/DATA4T/civitai"
    data_dir = f"{data_base}/data"
    total_pages = 632
    cur_page_num = 1
    start_urls = ["https://civitai.com/api/v1/models?page=1"]


    def start_requests(self):
        os.makedirs(self.meta_dir, exist_ok=True)
        return [Request(url, callback=self.parse) for url in self.start_urls]

    def parse(self, response: HtmlResponse):
        yield 
