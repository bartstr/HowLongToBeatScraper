from datetime import date, datetime
import logging
import os
from pathlib import Path
import re
import scrapy
from scrapy.http import FormRequest, Request


"""
Import atrocity below is caused pycharm import path difference between running live spider and scrap_tests.py module
"""
if __name__ != 'how_long_to_beat_spiders':
    from how_long_to_beat.how_long_to_beat.items import HowLongToBeatItem
    from how_long_to_beat.how_long_to_beat.utils.completion_time_utils import fraction_normalisation
    from how_long_to_beat.how_long_to_beat.utils.date_utils import release_date_normalisation
else:
    from how_long_to_beat.items import HowLongToBeatItem
    from how_long_to_beat.utils.completion_time_utils import fraction_normalisation
    from how_long_to_beat.utils.date_utils import release_date_normalisation


log_filename = os.path.join(Path(os.getcwd()).parent, 'logs', f'how_long_to_beat_{date.today()}.log')
file_handler = logging.FileHandler(filename=log_filename, mode='a')
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger = logging.getLogger('HLTB')
logger.addHandler(file_handler)


class HowLongToBeat(scrapy.Spider):

    print(f'NAME: {__name__}')

    name = 'hltb_spider'
    start_urls = [f'https://howlongtobeat.com/search_results?page={x}' for x in range(1, 3879)]
    domain = 'https://howlongtobeat.com'

    def start_requests(self):
        logger.info(f'Started crawling {self.domain} at {datetime.now()}')
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
            logger.info(f'Crawling {url}.')
            yield FormRequest(url=url, formdata=data, callback=self.parse_search_page, method='POST')

    def parse_search_page(self, response):
        games_internal_links = response.xpath('//h3[@class="shadow_text"]/a[@class="text_white"]/@href')
        for link in games_internal_links:
            yield Request(f'{self.domain}/{link.get()}', self.parse_game_data)

    def __name_parser(self, response):
        try:
            raw_name = \
            response.xpath('//div[@class="profile_header_game"]/div[contains(@class, "profile_header")]/text()').get()
            name_without_trailing_and_leading_whitespaces = re.sub(r'^[\s]+|[\s]+$', '', raw_name)
            clean_name = re.sub(r'\s+', ' ', name_without_trailing_and_leading_whitespaces)
            return clean_name
        except Exception as e:
            logger.warning(f'Failed to scrap name at {response.url}. {e}')

    def __platforms_parser(self, response):
        try:
            raw_platforms = response.xpath \
            ('//div[contains(@class, "profile_info")]/strong[contains(text(), "Platform")]/following-sibling::text()[2]'). \
            get()
            platforms = [x.strip() for x in raw_platforms.split(",")]
            return platforms
        except Exception as e:
            logger.warning(f'Failed to scrap platforms at {response.url}. {e}')

    def __genres_parser(self, response):
        try:
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
        except Exception as e:
            logger.warning(f'Failed to scrap genres at {response.url}. {e}')

    def __developer_parser(self, response):
        try:
            developer_raw = response.xpath(
                '//div[contains(@class, "profile_info")]/strong[contains(text(), "Developer")]/following-sibling::text()[2]').get()
            return developer_raw.strip()
        except Exception as e:
            logger.warning(f'Failed to scrap developer at {response.url}. {e}')

    def __publisher_parser(self, response):
        try:
            publisher_raw = response.xpath(
                '//div[contains(@class, "profile_info")]/strong[contains(text(), "Publisher")]/following-sibling::text()[2]').get()
            return publisher_raw.strip()
        except Exception as e:
            logger.warning(f'Failed to scrap publisher at {response.url}. {e}')

    def __release_date_parser(self, response):
        try:
            release_dates_raw = response.xpath(
                '//div[contains(@class, "profile_info")]/strong[contains(text(), "NA") or contains(text(), "EU") or contains(text(), "JP")]/following-sibling::text()[2]').getall()
            release_dates = []
            for raw_date in release_dates_raw:
                clean_date = raw_date.strip()
                release_dates.append(clean_date)
            clean_date = release_date_normalisation(release_dates).__str__()
            return clean_date
        except Exception as e:
            logger.warning(f'Failed to scrap release date at {response.url}. {e}')

    def __rating_parser(self, response):
        try:
            rating_raw = response.xpath('//div[@class="profile_details"]//li[contains(text(), "Rating")]').get()
            rating = re.findall(r'\d+', rating_raw)
            return int(rating[0])
        except Exception as e:
            logger.warning(f'Failed to scrap rating at {response.url}. {e}')

    def __main_story_parser(self, response):
        try:
            main_story_raw = response.xpath(
                '//li[contains(@class, "short")]/*[contains(text(), "Main Story")]/following-sibling::div/text()').get()
            return fraction_normalisation(main_story_raw)
        except Exception as e:
            logger.warning(f'Failed to scrap main story at {response.url}. {e}')

    def __main_plus_extras_parser(self, response):
        try:
            main_plus_extras_raw = response.xpath(
                '//li[contains(@class, "short")]/*[contains(text(), "Main + Extras")]/following-sibling::div/text()').get()
            return fraction_normalisation(main_plus_extras_raw)
        except Exception as e:
            logger.warning(f'Failed to scrap main plus extras at {response.url}. {e}')

    def __completionist_parser(self, response):
        try:
            completionist_raw = response.xpath(
                '//li[contains(@class, "short")]/*[contains(text(), "Completionist")]/following-sibling::div/text()').get()
            return fraction_normalisation(completionist_raw)
        except Exception as e:
            logger.warning(f'Failed to scrap completionist at {response.url}. {e}')

    def __all_styles_parser(self, response):
        try:
            all_styles_raw = response.xpath(
                '//li[contains(@class, "short")]/*[contains(text(), "All Styles")]/following-sibling::div/text()').get()
            return fraction_normalisation(all_styles_raw)
        except Exception as e:
            logger.warning(f'Failed to scrap all styles at {response.url}. {e}')

    def parse_game_data(self, response):
        item = HowLongToBeatItem()

        item['name'] = self.__name_parser(response)
        item['platforms'] = self.__platforms_parser(response)
        item['genres'] = self.__genres_parser(response)
        item['developer'] = self.__developer_parser(response)
        item['publisher'] = self.__publisher_parser(response)
        item['release_date'] = self.__release_date_parser(response)
        item['rating'] = self.__rating_parser(response)
        item['main_story'] = self.__main_story_parser(response)
        item['main_plus_extras'] = self.__main_plus_extras_parser(response)
        item['completionist'] = self.__completionist_parser(response)
        item['all_styles'] = self.__all_styles_parser(response)

        yield item
