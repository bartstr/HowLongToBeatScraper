import scrapy
from how_long_to_beat.items import HowLongToBeatItem
import re
from scrapy.http import FormRequest, Request

from how_long_to_beat.utils.completion_time_utils import fraction_normalisation
from how_long_to_beat.utils.date_utils import release_date_normalisation


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
        release_dates_raw = response.xpath('//div[contains(@class, "profile_info")]/strong[contains(text(), "NA") or contains(text(), "EU") or contains(text(), "JP")]/following-sibling::text()[2]').getall()
        release_dates = []
        for raw_date in release_dates_raw:
            clean_date = raw_date.strip()
            release_dates.append(clean_date)
        item['release_date'] = release_date_normalisation(release_dates).__str__()
        rating_raw = response.xpath('//div[@class="profile_details"]//li[contains(text(), "Rating")]').get()
        rating = re.findall('\d+', rating_raw)
        item['rating'] = int(rating[0])
        main_story_raw = response.xpath('//li[@class="short time_100"]/*[contains(text(), "Main Story")]/following-sibling::div/text()').get()
        item['main_story'] = fraction_normalisation(main_story_raw)
        main_plus_extras_raw = response.xpath('//li[@class="short time_100"]/*[contains(text(), "Main + Extras")]/following-sibling::div/text()').get()
        item['main_plus_extras'] = fraction_normalisation(main_plus_extras_raw)
        completionist_raw = response.xpath(
            '//li[@class="short time_100"]/*[contains(text(), "Completionist")]/following-sibling::div/text()').get()
        item['completionist'] = fraction_normalisation(completionist_raw)
        all_styles_raw = response.xpath(
            '//li[@class="short time_100"]/*[contains(text(), "All Styles")]/following-sibling::div/text()').get()
        item['all_styles'] = fraction_normalisation(all_styles_raw)
        yield item




