# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ImageItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    urls = Field()
    base_model = Field() # main id of model
    model_version = Field() # versions of id of model
    data_base = Field()



class ModelItem(Item):
    url = Field()
    base_model = Field()
    model_version = Field()
    data_base = Field()
    
