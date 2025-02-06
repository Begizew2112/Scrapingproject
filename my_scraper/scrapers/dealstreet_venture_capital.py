import time
import csv
import os
import json
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException
)
from scrapers.base_scraper import BaseScraper
from utils.db_utils import insert_page_data  # If needed

class DealStreetScraper(BaseScraper):
    def __init__(self, headless=True, language="en"):
        super().__init__(headless, language)   # Use base scraper's initialization
        self.base_url = "https://www.dealstreetasia.com/section/venture-capital"
        self.csv_filename = "dealstreet_capital.csv"
        self.progress_file = "dealstreet_capital.json"
        self.two_months_ago = datetime.now() - timedelta(days=60)
        # Write CSV header
        with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Source", "Date", "Article Content", "URL"])

    def open_website(self):
        """Opens the DealStreetAsia Private Equity page."""
        self.driver.get(self.base_url)
        time.sleep(3)

    def wait_for_element(self, xpath, timeout=10):
        """Wait for an element to appear and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def click_element(self, xpath, timeout=10):
        """Wait for an element to be clickable and click it."""
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
        return element

    def parse_and_format_date(self, date_str):
        """Parses and reformats the date from the article."""
        try:
            # Format: "15 January, 2025" → "15 ,01, 2025"
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
                print("Warning: Progress file is empty or corrupted. Starting from scratch.")
        return None

    def save_progress(self, last_scraped_url):
        """Save the last scraped article URL to the progress file."""
        with open(self.progress_file, 'w') as f:
            json.dump({"last_scraped_url": last_scraped_url}, f)

    def scrape_article(self, link):
        """Scrape data from a single article given its URL."""
        self.driver.get(link)
        time.sleep(2)
        try:
            title = self.wait_for_element('//*[@id="disable-copy"]/h1', timeout=10).text.strip()
            source = self.wait_for_element('//*[@id="disable-copy"]/div[2]/div[1]/div/div[1]/span/a', timeout=10).text.strip()
            date_text = self.wait_for_element('//*[@id="disable-copy"]/div[2]/div[1]/div/div[1]/p', timeout=10).text.strip()
            body = self.wait_for_element('//*[@id="disable-copy"]/div[2]/div[2]/div[1]/article', timeout=10).text.strip().replace("\n", " ")
            
            formatted_date = self.parse_and_format_date(date_text)
            if not formatted_date:
                return None  # Skip article if date cannot be parsed
            article_date = datetime.strptime(formatted_date, "%d ,%m, %Y")
            
            # Check date threshold
            if article_date < self.two_months_ago:
                print(f"⏹️ Stopping: Found an article older than 2 months ({formatted_date})")
                return "STOP"
            
            # Return data as a tuple
            return (title, source, formatted_date, body, link)
        except Exception as e:
            print(f"Error extracting article data from {link}: {e}")
            return None

    def process_articles_on_page(self):
        """Process all articles on the current page."""
        # Find all article containers
        try:
            articles = self.driver.find_elements(By.XPATH, '//*[@id="archive-wrapper"]/div[4]/div[1]/div/div')
        except NoSuchElementException:
            print("No article containers found on this page.")
            return False

        # Extract links from articles
        article_links = []
        for article in articles:
            try:
                link = article.find_element(By.XPATH, './div[1]/a').get_attribute('href')
                article_links.append(link)
            except NoSuchElementException:
                continue  # Skip if link not found
    
        if not article_links:
            print("No article links found.")
            return False

        # Load progress and determine starting index
        last_scraped_url = self.load_progress()
        start_index = 0
        if last_scraped_url and last_scraped_url in article_links:
            start_index = article_links.index(last_scraped_url) + 1
        
        # Process articles starting from start_index
        for link in article_links[start_index:]:
            result = self.scrape_article(link)
            if result == "STOP":
                return False
            elif result:
                title, source, formatted_date, body, link = result
                # Write article data to CSV
                with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([title, source, formatted_date, body, link])
                print(f"Saved article: {title} - {formatted_date}")
                self.save_progress(link)
                # Navigate back to the list page (if needed)
                self.driver.back()
                time.sleep(2)
        return True

    def click_more_button(self):
        """Clicks the 'More' button to load additional articles."""
        try:
            more_button = self.wait_for_element('//*[@id="archive-wrapper"]/div[5]/div/button', timeout=10)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", more_button)
            time.sleep(5)
            return True
        except (NoSuchElementException, ElementClickInterceptedException) as e:
            print("No 'More' button found or can't be clicked. Stopping.")
            return False

    def run(self):
        """Main function to run the scraper."""
        try:
            self.open_website()
            time.sleep(3)
            # Open CSV header has been written in __init__
            while True:
                if not self.process_articles_on_page():
                    break
                if not self.click_more_button():
                    break
        finally:
            print(f"\nScraping complete! Data saved to {self.csv_filename}")
            self.driver.quit()

# To run the scraper, simply instantiate and run:
if __name__ == '__main__':
    scraper = DealStreetScraper(headless=False, language="en")
    scraper.run()
