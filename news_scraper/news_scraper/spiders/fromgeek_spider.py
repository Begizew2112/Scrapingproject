import scrapy
import time
class FromGeekSpider(scrapy.Spider):
    name = "fromgeek"
    allowed_domains = ["fromgeek.com"]
    start_urls = ["https://www.fromgeek.com/vc/"]

    def parse(self, response):
        # Loop through each article element (from li[7] to li[50])
        for article in response.xpath('//*[@id="lists"]/li[position() >= 7 and position() <=10]'):
            # Extract the link (usually <h4> contains the link text)
            time.sleep(2)
            article_url = article.xpath('div[1]/h4/a/@href').get()
            # Check if the article_url is complete, if not, add the base URL
            time.sleep(2)
            if article_url and not article_url.startswith('http'):
                article_url = response.urljoin(article_url)
            # Follow the article link to scrape its details
            yield response.follow(article_url, self.parse_article)
            time.sleep(2)

    def parse_article(self, response):
        # Extract article details from the article page
        title = response.xpath('/html/body/div[2]/div/div[1]/div/h1/text()').get()
        views = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[1]/text()').get()
        date = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[2]/text()').get()
        source = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[3]/text()').get()
        article_body = response.xpath('/html/body/div[2]/div/div[1]/div/div[2]/article//text()').getall()

        # Clean up article body text
        article_body = ' '.join(article_body).strip()

        # Store the scraped data
        yield {
            'title': title,
            'views': views,
            'date': date,
            'source': source,
            'article_body': article_body
        }

