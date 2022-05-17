# HowLongToBeatScraper

Scrapy based scraper to dump data about each game on this page.

For each game its downloads the following data:

Name

Platforms

Genres

Developer

Publisher

Earliest release date (howlongtobeat.com provides release dates for three different (if available) markets: US, EU and JP, my choice was to download the earliest of them no matter what market it is)

Rating

Completion time for:

Main story

Main story + some extras

Completionist

and all styles which is the median of all of the above.

All of these are encapsulated in scrapy own item entity.

To run scraper after downloading repo and installing requirements form requirements.txt use:

scrapy runspider ...\how_long_to_beat_spiders.py


To dump data to file start scraper with the following arguments (according to scrapy own documentation https://docs.scrapy.org/en/latest/topics/feed-exports.html#topics-feed-exports):

-o items.json for a json file.

-o items.csv for csv file.

-o items.xml for xml file.

Last actualization and scraping done 17th May 2022.
