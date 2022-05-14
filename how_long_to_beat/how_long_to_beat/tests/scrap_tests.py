from how_long_to_beat.how_long_to_beat.spiders import how_long_to_beat_spiders
import unittest
import os
from scrapy.selector import Selector

TEST_SEARCH_URL = os.path.join(os.getcwd() + '\\test_data\HowLongToBeat_com_search.html')
TEST_ELDEN_URL = os.path.join(os.getcwd() + '\\test_data\HowLongToBeat_com_elden.html')


class TestParsers(unittest.TestCase):

    def setUp(self):
        self.spider = how_long_to_beat_spiders.HowLongToBeat(limit=1)
        with open(TEST_SEARCH_URL, 'r') as f:
            test_search_page = f.read()
            self.search_page_html = Selector(text=str(test_search_page))

        with open(TEST_ELDEN_URL, 'r') as fi:
            test_game_page = fi.read()
            self.test_game_page_html = Selector(text=str(test_game_page))

    def test_parse_search_page(self):
        expected = {'https://howlongtobeat.com/https://howlongtobeat.com/game?id=68151',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=98273',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=68261',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=2127',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=10469',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=79775',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=10270',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=72584',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=7231',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=26286',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=62941',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=1065',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=4064',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=7230',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=27100',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=38050',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=89107',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=53247',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=52546',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=1068',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=68151',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=98273',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=68261',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=2127',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=10469',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=79775',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=94135',
                    'https://howlongtobeat.com/https://howlongtobeat.com/game?id=80122'}
        result = self.spider.parse_search_page(self.search_page_html)
        results = set()
        for i in result:
            results.add(i.url)
        self.assertEqual(results, expected)

    def test_parse_game_data(self):
        expected_game_name = 'Elden Ring'
        expected_platforms = ['PC', 'PlayStation 4', 'PlayStation 5', 'Xbox One', 'Xbox Series X/S']
        expected_genres = ['Third-Person', 'Action', 'Open World', 'Role-Playing']
        expected_developer = 'FromSoftware'
        expected_publisher = 'Bandai Namco Entertainment'
        expected_release_date = '2022-02-25'
        expected_rating = 93
        expected_main_story = 50
        expected_main_plus_extras = 93
        expected_completionist = 126
        expected_all_styles = 100
        result = self.spider.parse_game_data(self.test_game_page_html)
        for i in result:
            self.assertEqual(i['name'], expected_game_name)
            self.assertEqual(i['platforms'], expected_platforms)
            self.assertEqual(i['genres'], expected_genres)
            self.assertEqual(i['developer'], expected_developer)
            self.assertEqual(i['publisher'], expected_publisher)
            self.assertEqual(i['release_date'], expected_release_date)
            self.assertEqual(i['rating'], expected_rating)
            self.assertEqual(i['main_story'], expected_main_story)
            self.assertEqual(i['main_plus_extras'], expected_main_plus_extras)
            self.assertEqual(i['completionist'], expected_completionist)
            self.assertEqual(i['all_styles'], expected_all_styles)


if __name__ == '__main__':
    unittest.main()
