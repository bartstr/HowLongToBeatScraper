import scrapy
from how_long_to_beat.items import HowLongToBeatItem
import re
from scrapy.http import FormRequest, Request


class HowLongToBeat(scrapy.Spider):
    name = 'hltb_spider'
    start_urls = [f'https://howlongtobeat.com/search_results?page={x}' for x in range(1, 2)] # 2679
    domain = 'https://howlongtobeat.com'

    """
    custom_settings = {
        'DUPEFILTER_DEBUG': False,
    }
    """

    def start_requests(self):
        data = {
            'queryString': '',
            't': 'games',
            'sorthead': 'popular',
            'sortd': '0',
            'plat': '',
            'length_type': 'main',
            'length_min': '',
            'length_max': '',
            'v': '',
            'f': '',
            'g': '',
            'detail': '',
            'randomize': '0',
        }
        headers = {
            'referer': 'https://howlongtobeat.com/',
            'origin': 'https://howlongtobeat.com/',
            'Accept': '*/*',
        }
        for url in self.start_urls:
            yield FormRequest(url=url, formdata=data, callback=self.parse_search_page, method='POST')

    def parse_search_page(self, response):
        games_internal_links = response.xpath('//h3[@class="shadow_text"]/a[@class="text_white"]/@href')
        for link in games_internal_links:
            yield Request(f'{self.domain}/{link.get()}', self.parse_game_data)

    def parse_game_data(self, response):
        item = HowLongToBeatItem()
        raw_name = \
            response.xpath('//div[@class="profile_header_game"]/div[contains(@class, "profile_header")]/text()').get()
        clean_name = re.sub('\s+', ' ', raw_name)
        item['name'] = clean_name
        raw_platforms = response.xpath\
            ('//div[contains(@class, "profile_info")]/strong[contains(text(), "Platform")]/following-sibling::text()[2]').\
            get()
        platforms = [x.strip() for x in raw_platforms.split(",")]
        item['platforms'] = platforms
        raw_genres = response.xpath('//div[contains(@class, "profile_info")]/strong[contains(text(), "Genre")]/following-sibling::text()[2]').get()
        genres = [x.strip() for x in raw_genres.split(",")]
        item['genres'] = genres
        developer_raw = response.xpath('//div[contains(@class, "profile_info")]/strong[contains(text(), "Developer")]/following-sibling::text()[2]').get()
        item['developer'] = developer_raw.strip()
        publisher_raw = response.xpath('//div[contains(@class, "profile_info")]/strong[contains(text(), "Publisher")]/following-sibling::text()[2]').get()
        item['publisher'] = publisher_raw.strip()
        print(item)
        # https://www.youtube.com/watch?v=kkWhQKtxT2I&ab_channel=buildwithpython


