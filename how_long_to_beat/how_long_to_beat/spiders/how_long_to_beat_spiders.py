import scrapy

import re
from scrapy.http import FormRequest, Request
"""
from how_long_to_beat.how_long_to_beat.items import HowLongToBeatItem
from how_long_to_beat.how_long_to_beat.utils.completion_time_utils import fraction_normalisation
from how_long_to_beat.how_long_to_beat.utils.date_utils import release_date_normalisation
"""
from how_long_to_beat.items import HowLongToBeatItem
from how_long_to_beat.utils.completion_time_utils import fraction_normalisation
from how_long_to_beat.utils.date_utils import release_date_normalisation


class HowLongToBeat(scrapy.Spider):
    name = 'hltb_spider'
    start_urls = [f'https://howlongtobeat.com/search_results?page={x}' for x in range(1, 3879)]
    domain = 'https://howlongtobeat.com'

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
        for url in self.start_urls:
            yield FormRequest(url=url, formdata=data, callback=self.parse_search_page, method='POST')

    def parse_search_page(self, response):
        games_internal_links = response.xpath('//h3[@class="shadow_text"]/a[@class="text_white"]/@href')
        for link in games_internal_links:
            yield Request(f'{self.domain}/{link.get()}', self.parse_game_data)

    def _name_parser(self, response):
        raw_name = \
            response.xpath('//div[@class="profile_header_game"]/div[contains(@class, "profile_header")]/text()').get()
        name_without_trailing_and_leading_whitespaces = re.sub(r'^[\s]+|[\s]+$', '', raw_name)
        clean_name = re.sub(r'\s+', ' ', name_without_trailing_and_leading_whitespaces)
        return clean_name

    def _platforms_pareser(self, response):
        raw_platforms = response.xpath \
            ('//div[contains(@class, "profile_info")]/strong[contains(text(), "Platform")]/following-sibling::text()[2]'). \
            get()
        platforms = [x.strip() for x in raw_platforms.split(",")]
        return platforms

    def _genres_parser(self, response):
        raw_genre = response.xpath(
            '//div[contains(@class, "profile_info")]/strong[contains(text(), "Genre")]/following-sibling::text()[2]').get()
        raw_genres = response.xpath(
            '//div[contains(@class, "profile_info")]/strong[contains(text(), "Genres")]/following-sibling::text()[2]').get()
        if raw_genre:
            genres = [x.strip() for x in raw_genre.split(",")]
        elif raw_genres:
            genres = [x.strip() for x in raw_genres.split(",")]
        else:
            genres = None
        return genres

    def _developer_parser(self, response):
        developer_raw = response.xpath(
            '//div[contains(@class, "profile_info")]/strong[contains(text(), "Developer")]/following-sibling::text()[2]').get()
        return developer_raw.strip()

    def _publisher_parser(self, response):
        publisher_raw = response.xpath(
            '//div[contains(@class, "profile_info")]/strong[contains(text(), "Publisher")]/following-sibling::text()[2]').get()
        return publisher_raw.strip()

    def _release_date_parser(self, response):
        release_dates_raw = response.xpath(
            '//div[contains(@class, "profile_info")]/strong[contains(text(), "NA") or contains(text(), "EU") or contains(text(), "JP")]/following-sibling::text()[2]').getall()
        release_dates = []
        for raw_date in release_dates_raw:
            clean_date = raw_date.strip()
            release_dates.append(clean_date)
        clean_date = release_date_normalisation(release_dates).__str__()
        return clean_date

    def _rating_parser(self, response):
        rating_raw = response.xpath('//div[@class="profile_details"]//li[contains(text(), "Rating")]').get()
        rating = re.findall(r'\d+', rating_raw)
        return int(rating[0])

    def _main_story_parser(self, response):
        main_story_raw = response.xpath(
            '//li[contains(@class, "short")]/*[contains(text(), "Main Story")]/following-sibling::div/text()').get()
        return fraction_normalisation(main_story_raw)

    def _main_plus_extras_parser(self, response):
        main_plus_extras_raw = response.xpath(
            '//li[contains(@class, "short")]/*[contains(text(), "Main + Extras")]/following-sibling::div/text()').get()
        return fraction_normalisation(main_plus_extras_raw)

    def _completionist_parser(self, response):
        completionist_raw = response.xpath(
            '//li[contains(@class, "short")]/*[contains(text(), "Completionist")]/following-sibling::div/text()').get()
        return fraction_normalisation(completionist_raw)

    def _all_styles_parser(self, response):
        all_styles_raw = response.xpath(
            '//li[contains(@class, "short")]/*[contains(text(), "All Styles")]/following-sibling::div/text()').get()
        return fraction_normalisation(all_styles_raw)

    def parse_game_data(self, response):
        item = HowLongToBeatItem()
        item['name'] = self._name_parser(response)
        item['platforms'] = self._platforms_pareser(response)
        item['genres'] = self._genres_parser(response)
        item['developer'] = self._developer_parser(response)
        item['publisher'] = self._publisher_parser(response)
        item['release_date'] = self._release_date_parser(response)
        item['rating'] = self._rating_parser(response)
        item['main_story'] = self._main_story_parser(response)
        item['main_plus_extras'] = self._main_plus_extras_parser(response)
        item['completionist'] = self._completionist_parser(response)
        item['all_styles'] = self._all_styles_parser(response)

        yield item
