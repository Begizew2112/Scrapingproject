import csv
import time
import json
import os
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapers.base_scraper import BaseScraper
from utils.selenium_utils import wait_for_element

class VCCirclePEScraper(BaseScraper):
    def __init__(self, headless=True):
        super().__init__(headless)
        self.website = "https://www.vccircle.com/deal-type/pe"
        self.csv_filename = "vccircle_pe.csv"
        self.progress_file = "vccircle_pe_progress.json"  # Store last scraped URL and page
        self.two_months_ago = datetime.now() - timedelta(days=60)
        self.scraped_urls = set()  # Keep track of scraped URLs to avoid duplicates

    def _init_csv(self):
        """Initialize CSV file with headers if it doesn't already exist."""
        if not os.path.exists(self.csv_filename):
            with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Source", "Date", "Article Content", "URL"])

    def parse_and_format_date(self, date_str):
        """Convert '14 January, 2025' into '14 - 01 - 2025'."""
        try:
            parsed_date = datetime.strptime(date_str, "%d %B, %Y")
            return parsed_date.strftime("%d - %m - %Y")
        except ValueError:
            return None

    def load_progress(self):
        """Load last scraped article URL and page number from the progress file."""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                return data.get("last_scraped_url"), data.get("page_number", 1)  # Default to page 1 if not found
        return None, 1  # Start from the first page and no last scraped URL

    def save_progress(self, last_scraped_url, page_number):
        """Save last scraped article URL and page number to progress file."""
        with open(self.progress_file, 'w') as f:
            json.dump({"last_scraped_url": last_scraped_url, "page_number": page_number}, f)

    def get_page_number_by_url(self, url):
        """Given a URL, find the page number where this article is located."""
        self.open_page(self.website)  # Go to the first page
        page_number = 1
        while True:
            articles = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div')
            for article in articles:
                article_url = article.find_element(By.XPATH, './div/div[2]/h4/a').get_attribute("href")
                if article_url == url:
                    return page_number  # Return the page number where the URL was found
            try:
                pagination_buttons = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/ul/li/a')
                if pagination_buttons:
                    next_button = pagination_buttons[-1]  # Select last pagination button
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(3)
                    self.driver.execute_script("arguments[0].click();", next_button)
                    page_number += 1
                    time.sleep(5)
                else:
                    break  # No more pages, stop the loop
            except NoSuchElementException:
                break  # No pagination buttons, stop the loop
        return None  # URL not found (shouldn't happen unless it's removed)

    def scrape_articles(self):
        """Scrape articles from VCCircle PE section."""
        last_scraped_url, page_number = self.load_progress()

        # If there's no last scraped URL, start from the first page
        if last_scraped_url is None:
            self.open_page(f"{self.website}?page={page_number}")
        else:
            # Get the page number where the last scraped URL is located
            page_number = self.get_page_number_by_url(last_scraped_url)
            if page_number:
                print(f"Resuming from page {page_number}, article {last_scraped_url}")
                self.open_page(f"{self.website}?page={page_number}")
        
        last_article_old = False

        while not last_article_old:
            try:
                wait_for_element(self.driver, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div')
            except TimeoutException:
                print("Page took too long to load. Stopping.")
                break

            articles = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div')
            
            for index, article in enumerate(articles):
                try:
                    date_text = article.find_element(By.XPATH, './div/div[2]/div/div').text.strip()
                    url = article.find_element(By.XPATH, './div/div[2]/h4/a').get_attribute("href")
                    
                    # Skip this article if it's already been scraped
                    if url in self.scraped_urls:
                        continue

                    title = article.find_element(By.XPATH, './div/div[2]/h4').text.strip()
                    body = article.find_element(By.XPATH, './div/div[2]/p').text.strip()
                    type_of_news = article.find_element(By.XPATH, './div/div[2]/div/h3/a').text.strip()
                    source = article.find_element(By.XPATH, './div/div[2]/ul/li/a').text.strip()

                    formatted_date = self.parse_and_format_date(date_text)
                    article_date = datetime.strptime(formatted_date, "%d - %m - %Y") if formatted_date else None

                    if article_date and article_date < self.two_months_ago:
                        print(f"Stopping: Found an old article from {formatted_date}.")
                        last_article_old = True
                        break

                    # Save article to CSV (and optionally to database)
                    with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([title, source, formatted_date, body, url])

                    self.scraped_urls.add(url)  # Add the URL to the set of scraped URLs
                    print(f"Saved Article {index+1}: {title} ({formatted_date})")
                    self.save_progress(url, page_number)  # Save progress after each article

                except NoSuchElementException:
                    print(f" Missing data in article {index+1}. Skipping.")
                    continue

            # If we haven't reached an old article, try to go to the next page
            if not last_article_old:
                try:
                    pagination_buttons = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/ul/li/a')
                    if pagination_buttons:
                        next_button = pagination_buttons[-1]  # Select last pagination button
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        time.sleep(3)
                        self.driver.execute_script("arguments[0].click();", next_button)
                        print("Clicked 'Next Page' button")
                        time.sleep(5)
                        page_number += 1  # Update the page number
                    else:
                        print("\nNo more pages found. Stopping.")
                        last_article_old = True
                except NoSuchElementException:
                    print("\nNo 'Next Page' button found. Stopping.")
                    last_article_old = True

        print("\n Scraping complete! Data saved to CSV.")
        self.close()


# import csv
# import time
# import json
# import os
# from datetime import datetime, timedelta
# from scrapers.base_scraper import BaseScraper
# from utils.selenium_utils import wait_for_element
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from utils.db_utils import insert_page_data

# class VCCirclePEScraper(BaseScraper):
#     def __init__(self, headless=True):
#         super().__init__(headless)
#         self.website = "https://www.vccircle.com/deal-type/pe"
#         self.csv_filename = "vccircle_pe.csv"
#         self.progress_file = "vccircle_pe_progress.json"  # Store last scraped URL
#         self.two_months_ago = datetime.now() - timedelta(days=60)

#     def _init_csv(self):
#             """Initialize CSV file with headers."""
#             with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
#                 writer = csv.writer(file)
#                 writer.writerow(["Title", "Source", "Date", "Article Content", "URL"])

#     def parse_and_format_date(self, date_str):
#         """Convert '14 January, 2025' into '14 - 01 - 2025'."""
#         try:
#             parsed_date = datetime.strptime(date_str, "%d %B, %Y")
#             return parsed_date.strftime("%d - %m - %Y")
#         except ValueError:
#             return None

#     def load_progress(self):
#         """Load last scraped article URL from the progress file."""
#         if os.path.exists(self.progress_file):
#             with open(self.progress_file, 'r') as f:
#                 data = json.load(f)
#                 return data.get("last_scraped_url")
#         return None
    
    
#     # def load_progress(self):
#     #     """Load the last progress (page number and article index) from the progress file."""
#     #     if os.path.exists(self.progress_file):
#     #         with open(self.progress_file, 'r') as f:
#     #             data = json.load(f)
#     #             return data.get("page_number", 1), data.get("article_index", 1)  # Default to page 1, article 1
#     #     return 1, 1  # Start from the first page, first article

#     # def save_progress(self, page_number, article_index):
#     #     """Save the current progress (page number and article index) to the progress file."""
#     #     with open(self.progress_file, 'w') as f:
#     #         json.dump({"page_number": page_number, "article_index": article_index}, f)


#     def save_progress(self, last_scraped_url):
#         """Save last scraped article URL to progress file."""
#         with open(self.progress_file, 'w') as f:
#             json.dump({"last_scraped_url": last_scraped_url}, f)

#     def scrape_articles(self):
#         """Scrape articles from VCCircle PE section."""
#         self.open_page(self.website)
#         last_scraped_url = self.load_progress()
#         start_scraping = False  # Flag to resume from last progress

#         with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             if os.stat(self.csv_filename).st_size == 0:
#                 writer.writerow(["Date", "Title", "Body", "URL", "Type", "Source"])  # CSV Header
#         last_article_old = False

#         while not last_article_old:
#             try:
#                 wait_for_element(self.driver, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div')
#             except TimeoutException:
#                 print("Page took too long to load. Stopping.")
#                 break

#             articles = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div')
            
#             for index, article in enumerate(articles):
#                 try:
#                     date_text = article.find_element(By.XPATH, './div/div[2]/div/div').text.strip()
#                     url = article.find_element(By.XPATH, './div/div[2]/h4/a').get_attribute("href")
#                     title = article.find_element(By.XPATH, './div/div[2]/h4').text.strip()
#                     body = article.find_element(By.XPATH, './div/div[2]/p').text.strip()
#                     type_of_news = article.find_element(By.XPATH, './div/div[2]/div/h3/a').text.strip()
#                     source = article.find_element(By.XPATH, './div/div[2]/ul/li/a').text.strip()

#                     formatted_date = self.parse_and_format_date(date_text)
#                     article_date = datetime.strptime(formatted_date, "%d - %m - %Y") if formatted_date else None

#                     if article_date and article_date < self.two_months_ago:
#                         print(f"Stopping: Found an old article from {formatted_date}.")
#                         last_article_old = True
#                         break

#                     # Convert headers to JSON format
#                     headers_json = json.dumps({"Content-Type": "text/html"})

#                     # Insert article data into PostgreSQL
#                     # insert_page_data(
#                     #     url=url,
#                     #     status="200",  # Assume 200 for now
#                     #     response_body=body,
#                     #     headers=headers_json,
#                     #     data=json.dumps({
#                     #         "date": formatted_date,
#                     #         "title": title,
#                     #         "type": type_of_news,
#                     #         "source": source
#                     #     })
#                     # )
                    
#                     print(f" Saved Article {index+1}: {title} ({formatted_date})")
#                     self.save_progress(url)  # Save progress after each article

#                 except NoSuchElementException:
#                     print(f" Missing data in article {index+1}. Skipping.")
#                     continue

#             if last_article_old:
#                 break

#             # Click "Next Page" button
#             try:
#                 pagination_buttons = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/ul/li/a')
#                 if pagination_buttons:
#                     next_button = pagination_buttons[-1]  # Select last pagination button
#                     self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
#                     time.sleep(3)
#                     self.driver.execute_script("arguments[0].click();", next_button)
#                     print("Clicked 'Next Page' button")
#                     time.sleep(5)
#                 else:
#                     print("\nNo more pages found. Stopping.")
#                     last_article_old = True
#             except NoSuchElementException:
#                 print("\nNo 'Next Page' button found. Stopping.")
#                 last_article_old = True

#         print("\n Scraping complete! Data saved to PostgreSQL.")
#         self.close()
