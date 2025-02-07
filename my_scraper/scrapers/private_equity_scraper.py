import time
import csv
import os
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from scrapers.base_scraper import BaseScraper
from utils.db_utils import insert_page_data
from utils.selenium_utils import open_website
from utils.selenium_utils import parse_and_format_date
from utils.data_utils import load_progress
from utils.data_utils import save_progress
from utils.selenium_utils import click_more_button
#from utils.selenium_utils import create_selenium_driver
class PrivateEquityScraper(BaseScraper):
    def __init__(self, headless=True, language="en"):
        super().__init__(headless, language)   # Use base scraper's initialization
        self.base_url = "https://www.dealstreetasia.com/section/private-equity"
        self.csv_filename = "dealstreet_private_equity.csv"
        self.progress_file = "dealstreet_private_equity.json"
        self.two_months_ago = datetime.now() - timedelta(days=60)
        # Use the utility function to create the WebDriver
      #  self.driver = create_selenium_driver(headless)

    def scrape_articles(self):
        try:
            self.open_page(self.base_url)
            time.sleep(3)

            # Load last scraped URL
            #last_scraped_url = self.load_progress()
            last_scraped_url = load_progress(self.progress_file)


            # Check if file exists and has data
            file_exists = os.path.exists(self.csv_filename)
            existing_urls = set()

            if file_exists:
                try:
                    existing_data = pd.read_csv(self.csv_filename)
                    existing_urls = set(existing_data["URL"].tolist())  # Store previously scraped URLs
                except Exception as e:
                    print(f"⚠ Warning: Could not read existing CSV ({e}). Starting fresh.")

            with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                # Write header only if the file doesn't exist or is empty
                if not file_exists or os.stat(self.csv_filename).st_size == 0:
                    writer.writerow(["Title", "Source", "Date", "Article Content", "URL"])

                last_article_old = False
                last_scraped_index = 0

                while not last_article_old:
                    articles = self.driver.find_elements(By.XPATH, '//*[@id="archive-wrapper"]/div[4]/div[1]/div/div')
                    article_links = [article.find_element(By.XPATH, './div[1]/a').get_attribute('href') for article in articles]

                    # Find the index of the last scraped article
                    if last_scraped_url:
                        try:
                            last_scraped_index = article_links.index(last_scraped_url) + 1
                        except ValueError:
                            last_scraped_index = 0

                    for i in range(last_scraped_index, len(article_links)):
                        link = article_links[i]

                        # Skip if already saved
                        if link in existing_urls:
                            print(f"Skipping already saved article: {link}")
                            continue

                        self.driver.get(link)
                        time.sleep(2)

                        try:
                            title = self.driver.find_element(By.XPATH, '//*[@id="disable-copy"]/h1').text.strip()
                            source = self.driver.find_element(By.XPATH, '//*[@id="disable-copy"]/div[2]/div[1]/div/div[1]/span/a').text.strip()
                            date_text = self.driver.find_element(By.XPATH, '//*[@id="disable-copy"]/div[2]/div[1]/div/div[1]/p').text.strip()
                            body = self.driver.find_element(By.XPATH, '//*[@id="disable-copy"]/div[2]/div[2]/div[1]/article').text.strip().replace("\n", " ")

                            #formatted_date = self.parse_and_format_date(date_text)
                            formatted_date = parse_and_format_date(date_text)

                            article_date = datetime.strptime(formatted_date, "%d ,%m, %Y") if formatted_date else None

                            if article_date and article_date < self.two_months_ago:
                                print(f" Stopping: Found an article older than 2 months ({formatted_date})")
                                last_article_old = True
                                break

                            writer.writerow([title, source, formatted_date, body, link])
                            print(f" Saved article: {title} - {formatted_date}")

                            #self.save_progress(link)  # Save progress after each successful write
                            save_progress(self.progress_file,link)


                        except Exception as e:
                            print(f" Error extracting article data from {link}: {e}")

                        last_scraped_index = i + 1
                        self.driver.back()
                        time.sleep(2)

                    if last_article_old:
                        break

                    #if not self.click_more_button():
                    if not click_more_button(self.driver):
                        break
        finally:
            print(f"\nScraping complete! Data saved to {self.csv_filename}")
            self.driver.quit()  # Ensures the driver is always closed
