import scrapy
import re
import json

class AuthorSpider(scrapy.Spider):
    name = "business"
    start_urls = ["https://guiaempresas.universia.es/localidad/BARCELONA/"]
    scraped_data = []

    def parse(self, response):

        # Check for CAPTCHA presence based on specific page content
        if response.css('div.captcha'):
            self.logger.warning("CAPTCHA detected on the page. Exiting spider.")
            return  # Exit the spider
        else:
            self.logger.warning("No CAPTCHA detected on the page.")

        

        business_page_links = response.css('table.ranking_einf tr a::attr(href)').getall()
        if not business_page_links:
            # Print a message when there are no more links to follow
            self.logger.info("No more links in this page")
        else:
            yield from response.follow_all(business_page_links, self.parse_business)

        pagination_links = response.css("li.arrow a")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_business(self, response):
        business_data = {
            "name": response.css("h1.localbusiness::text").get(),
            "address": response.css("span.street-address::text").get(),
            "type": response.css("td.td_ficha_univ:contains(' - ')::text").get()
        }
        self.scraped_data.append(business_data)
        yield business_data

    def closed(self, reason):
        # Write the scraped data to a JSON file when the spider is closed
        with open("businessScraped.json", "w") as json_file:
            json.dump(self.scraped_data, json_file, indent=2)