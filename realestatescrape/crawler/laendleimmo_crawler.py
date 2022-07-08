import scrapy
import random
from user_agents import USER_AGENTS
from datetime import datetime
from scrapy.crawler import CrawlerProcess
import pandas as pd
import numpy as np


class LaendleimmoApartmentListScraper(scrapy.Spider):
    name = "laendleimmo_apartment_list_scraper"

    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "FEED_EXPORT_ENCODING": "utf-8-sig",
    }

    apt_list_req_item = {
        "id": [],
        "link": [],
        "created_at": []
    }

    id_increment = 0

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
            self.id_increment += 1
            self.apt_list_req_item["id"].append(self.id_increment)
            self.apt_list_req_item["link"].append(item.css("a.js-ad-click::attr(href)").get())
            self.apt_list_req_item["created_at"].append(datetime.date(datetime.now()))


        """
        Iterate through all the pages (pagination)
        """
        for next_page in response.css("ul li.next a"):
            yield response.follow(
                next_page,
                self.parse,
                headers={"User-Agent": random.choice(USER_AGENTS)},
            )

        df = pd.DataFrame(data=self.apt_list_req_item)
        df = df.to_numpy()
        np.savetxt("realestatescrape/data/apt_dump.csv", df, fmt="%s", delimiter=";")
        """
        df.to_csv(
            "realestatescrape/data/apt_dump.csv", index_label="id"
        )
        """
        

class LaendleimmoApartmentEntryScraper(scrapy.Spider):
    name = "laendleimmo_apartment_entry_scraper"

    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "FEED_EXPORT_ENCODING": "utf-8-sig",
    }

    link_list = {
        "title": [],
        "price": [],
        "number_of_rooms": [],
        "apt_size": [],
        "district": [],
        "city": [],
        "street_address": [],
    }

    def start_requests(self):
        df = pd.read_csv("realestatescrape/data/apt_dump.csv")

        urlList = df["link"].to_list()

        for item in urlList:
            yield scrapy.Request(
                    url=item,
                    callback=self.parse,
                    headers={"User-Agent": random.choice(USER_AGENTS)}
                )

    def parse(self, response):
        for item in response.css("body div.take-left"):

            self.link_list["title"].append(
                item.xpath(
                    "//body/div[1]/div[11]/div/div[1]/div[2]/div[2]/div[1]/h1/text()"
                ).get()
            )
            self.link_list["price"].append(
                item.xpath(
                    "//body/div[1]/div[11]/div/div[1]/div[2]/div[2]/div[2]/div[1]/text()"
                ).get()
            )
            self.link_list["number_of_rooms"].append(
                item.xpath(
                    "//body/div[1]/div[11]/div/div[2]/div/div[1]/div/div[2]/div[2]/div/text()"
                ).get()
            )
            self.link_list["apt_size"].append(
                item.xpath(
                    "//body/div[1]/div[11]/div/div[2]/div/div[1]/div/div[3]/div[2]/div/text()"
                ).get()
            )
            self.link_list["district"].append(
                item.xpath(
                    "//body/div[1]/div[11]/div/div[1]/div[1]/p/a[2]/text()"
                ).get()
            )
            self.link_list["city"].append(
                item.xpath(
                    "//body/div[1]/div[11]/div/div[1]/div[1]/p/a[3]/text()"
                ).get()
            )

            street_address = item.xpath(
                "//body/div[1]/div[11]/div/div[1]/div[1]/p/text()[3]"
            ).get()
            self.link_list["street_address"].append(street_address)

            # yield self.link_list

        a = {
            "title": self.link_list["title"],
            "price": self.link_list["price"],
            "number_of_room": self.link_list["number_of_rooms"],
            "apt_size": self.link_list["apt_size"],
            "district": self.link_list["district"],
            "city": self.link_list["city"],
            "street_address": self.link_list["street_address"],
        }
        file_export = pd.DataFrame(data=a)
        file_export.drop_duplicates(subset=["title"]).to_csv(
            "realestatescrape/data/apt_data.csv", index_label="id"
        ).reset_index()
"""
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(LaendleimmoApartmentListScraper)
    process.crawl(LaendleimmoApartmentEntryScraper)
    process.start()
"""
