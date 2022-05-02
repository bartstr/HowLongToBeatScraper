# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HowLongToBeatItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    platforms = scrapy.Field()
    genres = scrapy.Field()
    developer = scrapy.Field()
    publisher = scrapy.Field()
    release_date = scrapy.Field()

    rating = scrapy.Field()
    main_story = scrapy.Field()
    main_plus_extras = scrapy.Field()
    completionist = scrapy.Field()
    all_styles = scrapy.Field()


