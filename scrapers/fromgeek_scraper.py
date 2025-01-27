import time
import csv
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from scrapers.base_scraper import BaseScraper  # Import BaseScraper

class FromGeekScraper(BaseScraper):
    def __init__(self, headless=True, source_lang="zh-CN", target_lang="en"):
        #Initialize BaseScraper with dynamic language support
        super().__init__(headless=headless, source_lang=source_lang, target_lang=target_lang)
        
        self.base_url = "https://www.fromgeek.com/vc/"
        self.csv_filename = "fromgeek_scraped_data.csv"

        #Get the date 2 months ago
        self.two_months_ago = datetime.now() - timedelta(days=60)

       # Open CSV file and write headers
        with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Article URL', 'Title', 'Date', 'Views', 'Source', 'Content'])

    def parse_article_date(self, date_text):
        try:
            return datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"Error parsing date: {e}")
            return None

    def click_next_page(self):
        """Click 'Next Page' button to continue pagination."""
        try:
            next_buttons = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[1]/div/div/div[2]/div[2]/a')
            if next_buttons:
                next_button = next_buttons[-1]
                if next_button.is_displayed() and next_button.is_enabled():
                    self.driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(5)  # Wait for page load
                    return True
            print("No 'Next Page' button found, stopping pagination.")
            return False
        except Exception as e:
            print(f"Error clicking 'Next Page' button: {e}")
            return False

    def scrape_articles(self):
        """Scrape articles from FromGeek website."""
        self.open_page(self.base_url)
        time.sleep(5)

        page_number = 1
        while True:
            print(f"Scraping page {page_number}...")

            i = 1
            while True:
                try:
                    #Locate article link
                    article_link = self.driver.find_element(By.XPATH, f'//*[@id="lists"]/li[{i}]/div[1]/h4/a')
                    article_url = article_link.get_attribute('href')

                   # Click article to open
                    article_link.click()
                    time.sleep(5)

                    #Extract article details
                    date_text = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[2]').text
                    article_date = self.parse_article_date(date_text)

                    #Stop if article is older than 2 months
                    if article_date and article_date < self.two_months_ago:
                        print(f"Reached an article older than 2 months ({article_date}), stopping...")
                        self.close()
                        return

                    title = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/h1').text
                    views = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[1]').text
                    source = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[3]').text
                    content = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/article/p[1]').text

                    #Save to CSV
                    with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([article_url, title, article_date.strftime('%Y-%m-%d %H:%M:%S'), views, source, content])

                    print(f"Scraped: {title} | Date: {article_date}")

                    #Go back to article list
                    self.driver.back()
                    time.sleep(4)
                    i += 1

                except Exception as e:
                    print(f"Error extracting article {i} on page {page_number}: {e}")
                    i += 1  # Skip and continue

            #After scraping all articles on the page, check if pagination should continue
            if not self.click_next_page():
                break

            page_number += 1

        print(f"Scraping completed. Data saved to '{self.csv_filename}'.")
        self.close()
