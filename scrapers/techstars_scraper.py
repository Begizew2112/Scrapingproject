import time
import csv
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapers.base_scraper import BaseScraper

class TechStarsScraper(BaseScraper):
    def __init__(self, headless=True, language="en"):
        super().__init__(headless, language)  # Use base scraper's initialization
        self.base_url = "https://www.techstars.com/newsroom"
        self.csv_filename = "techstars_scraped_articles.csv"
        self.two_months_ago = datetime.now() - timedelta(days=60)

        # Open CSV file and write headers
        with open(self.csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Title", "Body", "URL"])

    def scrape_articles(self):
        """Scrape articles from TechStars Newsroom."""
        self.open_page(self.base_url)
        time.sleep(3)  # Allow initial page to load

        stop_scraping = False  # Stop flag for old articles

        while not stop_scraping:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div'))
                )
            except TimeoutException:
                print("Page took too long to load. Stopping.")
                break

            articles = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div')
            print(f"Found {len(articles)} articles on this page.")

            for index, article in enumerate(articles):
                try:
                    date_text = article.find_element(By.XPATH, './div/a[1]').text.strip()
                    article_url = article.find_element(By.XPATH, './div/a[2]').get_attribute("href")
                    title = article.find_element(By.XPATH, './div/a[2]/h5').text.strip()
                    body = article.find_element(By.XPATH, './div/a[3]').text.strip()

                    # Convert date format
                    try:
                        article_date = datetime.strptime(date_text, "%b %d, %Y")
                        formatted_date = article_date.strftime("%Y-%m-%d")
                    except ValueError:
                        print(f"Invalid date format: {date_text}. Skipping article.")
                        continue

                    # Stop scraping if article is older than 2 months
                    if article_date < self.two_months_ago:
                        print(f"Stopping: Found an old article from {formatted_date}.")
                        stop_scraping = True
                        break

                    # Save article data
                    with open(self.csv_filename, mode="a", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow([formatted_date, title, body, article_url])
                    
                    print(f"Saved Article {index+1}: {title} ({formatted_date})")

                except NoSuchElementException:
                    print(f"Missing data in article {index+1}. Skipping.")
                    continue

            if stop_scraping:
                break

            # Click 'Next Page' button
            try:
                next_button = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[6]/div[7]/button/span[1]')
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(2)
                self.driver.execute_script("arguments[0].click();", next_button)
                print("Clicked 'Next Page' button")
                time.sleep(5)
            except NoSuchElementException:
                print("No more pages found. Stopping.")
                break

        print(f"\nScraping complete! Data saved to {self.csv_filename}")
        self.close()
