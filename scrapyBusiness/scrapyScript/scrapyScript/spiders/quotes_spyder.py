import scrapy
import json


class AuthorSpider(scrapy.Spider):
    name = "author"
    start_urls = ["https://quotes.toscrape.com/"]
    scraped_data = []

    def parse(self, response):
        author_page_links = response.css(".author + a")
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default="").strip()

        author_data = {
            "name": extract_with_css("h3.author-title::text"),
            "birthdate": extract_with_css(".author-born-date::text"),
            "bio": extract_with_css(".author-description::text"),
        }
        self.scraped_data.append(author_data)

    def closed(self, reason):
        # Write the scraped data to a JSON file when the spider is closed
        with open("authors.json", "w") as json_file:
            json.dump(self.scraped_data, json_file, indent=2)

