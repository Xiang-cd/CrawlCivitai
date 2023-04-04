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

meta_ = "/DATA4T/civitai/meta/{}.json"

class CiviModelSpider(scrapy.Spider):
    name = "civi_model"
    allowed_domains = ["civitai.com"]
    data_base = "/DATA4T/civitai"
    data_dir = f"{data_base}/data"
    total_pages = 1
    cur_page_num = 1
    start_urls = [f"https://civitai.com/api/v1/models?page={cur_page_num}"]
    download_clip = 300


    def start_requests(self):
        os.makedirs(self.data_dir, exist_ok=True)
        return [Request(url, callback=self.parse) for url in self.start_urls]

    def parse(self, response: HtmlResponse):
        self.logger.info(f"{self.cur_page_num}/{self.total_pages}")
        if self.cur_page_num > self.total_pages:
            return
        else:
            with open(meta_.format(self.cur_page_num), "r") as f:
                dic = json.loads(f.read())
                f.close()
        items = dic["items"]
        
        def get_status(item, name):
            assert name in ["downloadCount", "rating", "ratingCount", "commentCount", "favoriteCount"]
            return item["stats"][name]
        
        for item in items:
            downloadCount = get_status(item, "downloadCount")
            if downloadCount < self.download_clip:
                continue
            base_id = item["id"]
            self.logger.info(f"id:{base_id}")
            
            os.makedirs(f"{self.data_dir}/{base_id}", exist_ok=True)
            with open(f"{self.data_dir}/{base_id}/meta.json", "w") as f:
                f.write(json.dumps(item))
                f.close()
            
            for version in item["modelVersions"]:
                version_id = version["id"]
                yield ModelItem(
                    url = version["downloadUrl"],
                    base_model = base_id,
                    model_version = version_id,
                    data_base = self.data_dir
                )
                
                yield ImageItem(
                        urls = [image["url"] for image in version["images"]],
                        base_model = base_id,
                        model_version = version_id,
                        data_base = self.data_dir
                    )
        self.cur_page_num += 1