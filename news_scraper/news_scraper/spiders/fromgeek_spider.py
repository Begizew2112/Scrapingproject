# import scrapy

# class FromGeekSpider(scrapy.Spider):
#     name = "fromgeek"
#     allowed_domains = ["fromgeek.com"]
#     start_urls = ["https://www.fromgeek.com/vc/"]

#     def parse(self, response):
#         # Loop through each article element (from li[7] to li[50])
#         for article in response.xpath('//*[@id="lists"]/li[position() >= 7 and position() <= 50]'):
#             # Extract the link (usually <h4> contains the link text)
#             article_url = article.xpath('div[1]/h4/a/@href').get()
#             # Check if the article_url is complete, if not, add the base URL
#             if article_url and not article_url.startswith('http'):
#                 article_url = response.urljoin(article_url)
#             # Follow the article link to scrape its details
#             yield response.follow(article_url, self.parse_article)

#     def parse_article(self, response):
#         # Extract article details from the article page
#         title = response.xpath('/html/body/div[2]/div/div[1]/div/h1/text()').get()
#         views = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[1]/text()').get()
#         date = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[2]/text()').get()
#         source = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[3]/text()').get()
#         article_body = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/article//text()').getall()

#         # Clean up article body text
#         article_body = ' '.join(article_body).strip()

#         # Store the scraped data
#         yield {
#             'title': title,
#             'views': views,
#             'date': date,
#             'source': source,
#             'article_body': article_body
#         }
import scrapy
import time

class FromGeekSpider(scrapy.Spider):
    name = "fromgeek"
    allowed_domains = ["fromgeek.com"]
    start_urls = ["https://www.fromgeek.com/vc/"]

    def parse(self, response):
        # Wait for the page to load completely and change the language
        time.sleep(2)  # Simulate delay to allow translation

        # Extract the first 3 article links (or you can change the range for more/less)
        article_links = response.xpath('//*[@id="lists"]/li/div[1]/h4/a/@href').extract()[:3]  # Scrape first 3 articles

        for link in article_links:
            # Construct the full URL and follow the link
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        # Extract article data after translation
        title = response.xpath('/html/body/div[2]/div/div[1]/div/h1/text()').extract_first()
        views = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[1]/text()').extract_first()
        date = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[2]/text()').extract_first()
        source = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[3]/text()').extract_first()
        article_content = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/article/text()').extract()

        # Yield data to output
        yield {
            'title': title,
            'views': views,
            'date': date,
            'source': source,
            'content': ''.join(article_content).strip()  # Join content and clean it
        }
