import scrapy
import re
import json

class AuthorSpider(scrapy.Spider):
    name = "business_informa"
    start_urls = ["https://www.informa.es/directorio-empresas/Localidad_BARCELONA.html"]
    scraped_data = []

    def parse(self, response):

        # Check for CAPTCHA presence based on specific page content
        if response.css('div.captcha'):
            self.logger.warning("CAPTCHA detected on the page. Exiting spider.")
            return  # Exit the spider
        else:
            self.logger.warning("No CAPTCHA detected on the page.")
        

        business_page_links = response.css("td.nom_empresa a ::attr(href)").getall()
        if not business_page_links:
            # Print a message when there are no more links to follow
            self.logger.info("No more links in this page")
        else:
            yield from response.follow_all(business_page_links, self.parse_business)

        pagination_links = response.css("a.next")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_business(self, response):

        row = response.xpath('//tr[th[contains(text(), "CNAE")]]')
        
        if row:
            # Extract the text from the specific <td> element
            cnae_text = row.xpath('.//td/text()').get()
        else:
            cnae_text = None

        business_data = {
            "name": response.css("td.localbusiness::text").get(),
            "address": response.css("span.street-address::text").get(),
            "type": cnae_text
        }
        self.scraped_data.append(business_data)
        yield business_data

    def closed(self, reason):
        # Write the scraped data to a JSON file when the spider is closed
        with open("businessScraped.json", "w") as json_file:
            json.dump(self.scraped_data, json_file, indent=2)