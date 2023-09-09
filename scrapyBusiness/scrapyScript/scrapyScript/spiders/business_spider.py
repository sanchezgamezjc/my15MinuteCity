import scrapy
import re
import json

class AuthorSpider(scrapy.Spider):
    name = "business"
    start_urls = ["https://guiaempresas.universia.es/localidad/BARCELONA/"]
    scraped_data = []

    def parse(self, response):
        business_page_links = response.css('table.ranking_einf tr a::attr(href)').getall()
        yield from response.follow_all(business_page_links, self.parse_business)

        # pagination_links = response.css("li.arrow a")
        # yield from response.follow_all(pagination_links, self.parse)

    def parse_business(self, response):
        business_data = {
            "name": response.css("h1.localbusiness::text").get(),
            "address": response.css("span.street-address::text").get(),
            "type": response.css("td.td_ficha_univ:contains(' - ')::text").get()
        }
        self.scraped_data.append(business_data)
        yield business_data  # Corrected to yield the data

    def closed(self, reason):
        # Write the scraped data to a JSON file when the spider is closed
        with open("businessScraped.json", "w") as json_file:
            json.dump(self.scraped_data, json_file, indent=2)