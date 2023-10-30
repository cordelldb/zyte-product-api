from scrapy import Spider

class ZyteSpider(Spider):
    name = "zyte"
    
    start_urls = [
        "https://www.amazon.com/s?k=protein+shaker+bottle"
    ]
    
    def parse(self, response):
        next_page_links = response.css(".s-pagination-next::attr(href)")
        yield from response.follow_all(next_page_links)
        product_links = response.css("h2 a::attr(href)")
        for request in response.follow_all(product_links, callback=self.parse_product):
            request.meta["zyte_api_automap"] = {"product": True}
            yield request

    def parse_product(self, response):
        yield response.raw_api_response["product"]
        
        
        # yield {
        #     "product_id": response.css("#ASIN::attr(value)").get(),
        #     "product_title": response.css("#productTitle::text").get().strip(),
        #     "url": response.url,
        # }