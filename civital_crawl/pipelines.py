# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import os
import json
from scrapy import Request
from scrapy.http.response import Response
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from civital_crawl.items import *
import logging
import hashlib
from scrapy.utils.python import get_func_args, to_bytes

class MyImagePipeline(ImagesPipeline):
    
    def get_media_requests(self, item, info):
        if type(item) is ImageItem:
            for url in item["urls"]:
                yield Request(url, meta=dict(item))

    def file_path(self, request, response:Response=None, info=None, *, item=None):
        media_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        meta = request._meta
        return f"{meta['base_model']}/{meta['model_version']}/{media_guid}.jpg"
            

    def item_completed(self, results, item, info):
        if type(item) is not ImageItem:
            return item
        status = [x for ok, x in results if ok]
        fail_st = [x for ok, x in results if not ok]
        if len(fail_st) > 0:
            logging.warning(fail_st)

        with open(os.path.join(item["data_base"], str(item["base_model"]), str(item["model_version"]), "dowload_info.json"), "w") as f:
            f.write(json.dumps(status))
            f.write("\n")
            f.close()

        return item

class MyModelPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if type(item) is ModelItem:
            yield Request(item["url"], meta=dict(item))

    def file_path(self, request, response:Response=None, info=None, *, item=None):
        media_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        meta = request._meta
        return f"{meta['base_model']}/{meta['model_version']}/{media_guid}.model"
            

    def item_completed(self, results, item, info):
        if type(item) is not ModelItem:
            return item
        status = [x for ok, x in results if ok]
        fail_st = [x for ok, x in results if not ok]
        if len(fail_st) > 0:
            logging.warning(fail_st)

        with open(os.path.join(item["data_base"], str(item["base_model"]), str(item["model_version"]), "dowload_info.json"), "a") as f:
            f.write(json.dumps(status))
            f.write("\n")
            f.close()

        return item