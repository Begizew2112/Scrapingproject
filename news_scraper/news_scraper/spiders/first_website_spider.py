# import scrapy

# class TechStarsSpider(scrapy.Spider):
#     name = 'techstars'
#     allowed_domains = ['techstars.com']
#     start_urls = ['https://www.techstars.com/newsroom']

#     def parse(self, response):
#         # Loop through each article container on the page
#         for article in response.xpath('//*[@id="__next"]/div/div[2]/div[2]/div'):
#             # Extract the title, date, and body of the article using the provided XPaths
#             title = article.xpath('.//div/a[1]/h6/text()').get()
#             date = article.xpath('.//div/a[2]/h5/text()').get()
#             body = article.xpath('.//div/a[3]/p/span/text()').get()

#             # Get the URL of the article by combining the base URL with the relative URL of the article
#             article_url = article.xpath('.//div/a[1]/@href').get()  # Adjust XPath if needed
#             full_article_url = response.urljoin(article_url)

#             # Write the extracted data to the output (CSV format)
#             yield {
#                 'Title': title,
#                 'Date': date,
#                 'Body': body,
#                 'URL': full_article_url  # Add URL to the output
#             }

#         # Pagination handling: Scrape the next page if it exists
#         next_page = response.xpath('//a[@class="next"]/@href').get()
#         if next_page:
#             yield response.follow(next_page, self.parse)
