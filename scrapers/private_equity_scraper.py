import time
import csv
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv
import os
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from scrapers.base_scraper import BaseScraper
import json
from utils.db_utils import insert_page_data

class PrivateEquityScraper(BaseScraper):
    def __init__(self, headless=True, language="en"):
        super().__init__(headless, language)   # Use base scraper's initialization
        self.base_url = "https://www.dealstreetasia.com/section/private-equity"
        self.csv_filename = "dealstreet_private_equity.csv"
        self.progress_file = "dealstreet_private_equity.json"
        self.two_months_ago = datetime.now() - timedelta(days=60)

    def open_website(self):
        """Opens the DealStreetAsia Private Equity page."""
        self.driver.get(self.base_url)
        time.sleep(3)

    def parse_and_format_date(self, date_str):
        """Parses and reformats the date from the article."""
        try:
            return datetime.strptime(date_str, "%d %B, %Y").strftime("%d ,%m, %Y")
        except ValueError:
            print(f"⚠ Warning: Could not parse date '{date_str}', skipping article.")
            return None

    def load_progress(self):
        """Load the last scraped article URL from the progress file."""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    return data.get("last_scraped_url")
            except (json.JSONDecodeError, FileNotFoundError):
                print(" Warning: Progress file is empty or corrupted. Starting from scratch.")
                return None
        return None

    def save_progress(self, last_scraped_url):
        """Save the last scraped article URL to the progress file."""
        with open(self.progress_file, 'w') as f:
            json.dump({"last_scraped_url": last_scraped_url}, f)

    def scrape_articles(self):
        try:
            self.open_page(self.base_url)
            time.sleep(3)
            
            with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Source", "Date", "Article Content", "URL"])
                
                last_article_old = False
                last_scraped_index = 0
                
                last_scraped_url = self.load_progress()
                
                while not last_article_old:
                    articles = self.driver.find_elements(By.XPATH, '//*[@id="archive-wrapper"]/div[4]/div[1]/div/div')
                    article_links = [article.find_element(By.XPATH, './div[1]/a').get_attribute('href') for article in articles]
                    
                    if last_scraped_url:
                        try:
                            last_scraped_index = article_links.index(last_scraped_url) + 1  # Move to next article
                        except ValueError:
                            last_scraped_index = 0

                    for i in range(last_scraped_index, len(article_links)):
                        link = article_links[i]
                        self.driver.get(link)
                        time.sleep(2)
                        
                        try:
                            title = self.driver.find_element(By.XPATH, '//*[@id="disable-copy"]/h1').text.strip()
                            source = self.driver.find_element(By.XPATH, '//*[@id="disable-copy"]/div[2]/div[1]/div/div[1]/span/a').text.strip()
                            date_text = self.driver.find_element(By.XPATH, '//*[@id="disable-copy"]/div[2]/div[1]/div/div[1]/p').text.strip()
                            body = self.driver.find_element(By.XPATH, '//*[@id="disable-copy"]/div[2]/div[2]/div[1]/article').text.strip().replace("\n", " ")

                            formatted_date = self.parse_and_format_date(date_text)
                            article_date = datetime.strptime(formatted_date, "%d ,%m, %Y") if formatted_date else None

                            if article_date and article_date < self.two_months_ago:
                                print(f"⏹️ Stopping: Found an article older than 2 months ({formatted_date})")
                                last_article_old = True
                                break

                            writer.writerow([title, source, formatted_date, body, link])
                            print(f"Saved article: {title} - {formatted_date}")

                            self.save_progress(link)  # Save after successful write
                        
                        except Exception as e:
                            print(f"Error extracting article data from {link}: {e}")
                        
                        last_scraped_index = i + 1
                        self.driver.back()
                        time.sleep(2)
                    
                    if last_article_old:
                        break
                    
                    if not self.click_more_button():
                        break
        finally:
            print(f"\nScraping complete! Data saved to {self.csv_filename}")
            self.driver.quit()  # Ensures the driver is always closed

    def click_more_button(self):
        """Clicks the 'More' button to load additional articles."""
        try:
            more_button = self.driver.find_element(By.XPATH, '//*[@id="archive-wrapper"]/div[5]/div/button')
            self.driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", more_button)
            time.sleep(5)
            return True
        except (NoSuchElementException, ElementClickInterceptedException):
            print("No 'More' button found or can't be clicked. Stopping.")
            return False
