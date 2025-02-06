# import time
# import csv
# import json
# from datetime import datetime, timedelta
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from scrapers.base_scraper import BaseScraper
# from utils.db_utils import insert_page_data

# class TechStarsScraper(BaseScraper):
#     def __init__(self, headless=True, language="en"):
#         super().__init__(headless, language)
#         self.base_url = "https://www.techstars.com/newsroom"
#         self.csv_filename = "techstars_scraped_articles.csv"
#         self.progress_file = "techstars_progress.json"
#         self.two_months_ago = datetime.now() - timedelta(days=60)

#         # Open CSV file and write headers if new
#         try:
#             with open(self.csv_filename, "x", encoding="utf-8", newline="") as file:
#                 writer = csv.writer(file)
#                 writer.writerow(["Date", "Title", "Body", "URL"])
#         except FileExistsError:
#             pass  # File exists, do nothing

#     def save_progress(self, page_number, article_index):
#         """Save last scraped page number and article index."""
#         with open(self.progress_file, "w") as f:
#             json.dump({"page_number": page_number, "article_index": article_index}, f)

#     def load_progress(self):
#         """Load last scraped page number and article index."""
#         try:
#             with open(self.progress_file, "r") as f:
#                 progress = json.load(f)
#                 return progress.get("page_number", 1), progress.get("article_index", 0)
#         except (FileNotFoundError, json.JSONDecodeError):
#             return 1, 0  # Start from first page and first article if no progress

#     def scrape_articles(self):
#         """Scrape articles from TechStars Newsroom with progress tracking."""
#         last_page, last_article = self.load_progress()

#         self.open_page(self.base_url)
#         time.sleep(3)

#         stop_scraping = False
#         current_page = 1

#         while not stop_scraping:
#             try:
#                 WebDriverWait(self.driver, 10).until(
#                     EC.presence_of_all_elements_located((By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div'))
#                 )
#             except TimeoutException:
#                 print("Page took too long to load. Stopping.")
#                 break

#             articles = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div')
#             print(f"Found {len(articles)} articles on page {current_page}.")

#             for index, article in enumerate(articles):
#                 if current_page == last_page and index < last_article:
#                     continue  # Skip already scraped articles

#                 try:
#                     date_text = article.find_element(By.XPATH, './div/a[1]').text.strip()
#                     article_url = article.find_element(By.XPATH, './div/a[2]').get_attribute("href")
#                     title = article.find_element(By.XPATH, './div/a[2]/h5').text.strip()
#                     body = article.find_element(By.XPATH, './div/a[3]').text.strip()

#                     try:
#                         article_date = datetime.strptime(date_text, "%b %d, %Y")
#                         formatted_date = article_date.strftime("%Y-%m-%d")
#                     except ValueError:
#                         print(f"Invalid date format: {date_text}. Skipping article.")
#                         continue

#                     if article_date < self.two_months_ago:
#                         print(f"Stopping: Found an old article from {formatted_date}.")
#                         stop_scraping = True
#                         break

#                     # Save to CSV
#                     with open(self.csv_filename, "a", encoding="utf-8", newline="") as file:
#                         writer = csv.writer(file)
#                         writer.writerow([formatted_date, title, body, article_url])

#                      #Convert headers to JSON format

#                     # headers_json = json.dumps({"Content-Type": "text/html"})

#                     # # Insert article data into PostgreSQL
#                     # insert_page_data(
#                     #     url=article_url,
#                     #     status="200",  # Assume 200 for now
#                     #     response_body=body,
#                     #     headers=headers_json,
#                     #     data=json.dumps({
#                     #         "date": formatted_date,
#                     #         "title": title
#                     #     })
#                     # )
                    
#                     # Save progress after each successful article
#                     self.save_progress(current_page, index + 1)

#                     print(f"Saved Article {index+1}: {title} ({formatted_date})")
#                     time.sleep(3)

#                 except NoSuchElementException:
#                     print(f"Missing data in article {index+1}. Skipping.")
#                     continue

#             if stop_scraping:
#                 break

#             # Click 'Next Page' button
#             try:
#                 next_button = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div[6]/div[7]/button/span[1]')
#                 self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
#                 time.sleep(2)
#                 self.driver.execute_script("arguments[0].click();", next_button)
#                 print(f"Clicked 'Next Page' button. Moving to page {current_page + 1}")
#                 current_page += 1
#                 time.sleep(5)
#             except NoSuchElementException:
#                 print("No more pages found. Stopping.")
#                 break

#         print(f"\nScraping complete! Data saved to {self.csv_filename}")
#         self.close_driver()

import time
import csv
import json
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapers.base_scraper import BaseScraper

class TechStarsScraper(BaseScraper):
    def __init__(self, headless=True, language="en"):
        super().__init__(headless, language)
        self.base_url = "https://www.techstars.com/newsroom"
        self.csv_filename = "techstars_scraped_articles.csv"
        self.two_months_ago = datetime.now() - timedelta(days=60)

        # Open CSV file and write headers if new
        try:
            with open(self.csv_filename, "x", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Title", "Body", "HTML", "URL"])
        except FileExistsError:
            pass  # File exists, do nothing

    def scrape_articles(self):
        """Scrape articles from TechStars Newsroom."""
        self.open_page(self.base_url)
        time.sleep(3)
        
        # Start looping through the articles
        
        while True:
            articles = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div[2]/div[2]/div')
            print(f"Found {len(articles)} articles.")
            
            if not articles:
                print("No more articles to scrape. Stopping.")
                break

            for index, article in enumerate(articles):
                try:
                    # Extract article link
                    article_url = article.find_element(By.XPATH, './div/a[2]').get_attribute("href")
                    self.open_page(article_url)
                    time.sleep(3)

                    # Extract title, date, and body
                    title = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[1]/h3').text.strip()
                    date_text = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[1]/h6').text.strip()
                    body = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/p[1]').text.strip()
                    
                    # Extract HTML content of the article
                    article_html = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div[2]/div[1]').get_attribute("outerHTML")
                    
                    # Convert date format
                    try:
                        article_date = datetime.strptime(date_text, "%b %d, %Y")
                        formatted_date = article_date.strftime("%Y-%m-%d")
                    except ValueError:
                        print(f"Invalid date format: {date_text}. Skipping article.")
                        continue

                    if article_date < self.two_months_ago:
                        print(f"Stopping: Found an old article from {formatted_date}.")
                        break

                    # Save to CSV
                    with open(self.csv_filename, "a", encoding="utf-8", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([formatted_date, title, body, article_html, article_url])
                    
                    print(f"Saved Article {index+1}: {title} ({formatted_date})")
                    
                    self.driver.back()
                    time.sleep(6)

                except NoSuchElementException:
                    print(f"Missing data in article {index+1}. Skipping.")
                    continue

            # Click the "More" button if available, otherwise stop
            try:
                more_button = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[3]/div/button')
                more_button.click()
                time.sleep(5)
            except NoSuchElementException:
                print("No more articles to load. Stopping.")
                break

        print(f"\nScraping complete! Data saved to {self.csv_filename}")
        self.close_driver()
