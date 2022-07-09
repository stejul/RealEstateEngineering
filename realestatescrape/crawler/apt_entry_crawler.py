import scrapy
import random
from user_agents import USER_AGENTS
from datetime import datetime
from scrapy.crawler import CrawlerProcess
import pandas as pd
import numpy as np

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
        df = pd.read_csv("realestatescrape/data/apt_dump.csv", sep=";")

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
        df = pd.DataFrame(data=a).drop_duplicates().to_numpy()
        np.savetxt("realestatescrape/data/apt_data.csv", df, fmt="%s", delimiter=";")
        """
        file_export.drop_duplicates(subset=["title"]).to_csv(
            "realestatescrape/data/apt_data.csv", index_label="id"
        ).reset_index()
        """

