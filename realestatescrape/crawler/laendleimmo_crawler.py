import scrapy
import random
from user_agents import USER_AGENTS
from datetime import datetime


class LaendleimmoScraper(scrapy.Spider):
    name = "laendleimmo_apartment_scraper"

    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "FEED_EXPORT_ENCODING": "utf-8-sig",
    }

    def start_requests(self):
        urls = ["https://www.laendleimmo.at/mietobjekt/wohnung/vorarlberg"]

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers={"User-Agent": random.choice(USER_AGENTS)},
            )

    def parse(self, response):
        """
        Iterate through all the links
        """
        for item in response.css("div.list-content h2.title-block-mobile"):
            yield {
                "link": item.css("a.js-ad-click::attr(href)").get(),
                "request_header": response.request.headers.get("User-Agent"),
                "access_timestamp": f"{datetime.date(datetime.now())} {datetime.time(datetime.now())}",
            }

        """
        Iterate through all the pages (pagination)
        """
        for next_page in response.css("ul li.next a"):
            yield response.follow(
                next_page,
                self.parse,
                headers={"User-Agent": random.choice(USER_AGENTS)},
            )
