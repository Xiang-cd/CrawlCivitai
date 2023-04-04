import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
import json
import os
import re
# total page 692

class CiviMetaSpider(scrapy.Spider):
    name = "civi_meta"
    allowed_domains = ["civitai.com"]
    data_base = "/DATA4T/civitai"
    meta_dir = f"{data_base}/meta"
    init_page = 632
    total_pages = 692
    start_urls = [f"https://civitai.com/api/v1/models?page={i}" for i in range(init_page, total_pages + 1)]


    def start_requests(self):
        os.makedirs(self.meta_dir, exist_ok=True)
        self.logger.info(self.start_urls)
        return [Request(url, callback=self.parse) for url in self.start_urls]

    def parse(self, response: HtmlResponse):
        js = json.loads(response.text)
        page = re.findall(r"page=(\d+)", response.url)[0]
        
        self.logger.info(page)
        with open(f"{self.meta_dir}/{page}.json", "w") as f:
            f.write(json.dumps(js))
            f.close()        
