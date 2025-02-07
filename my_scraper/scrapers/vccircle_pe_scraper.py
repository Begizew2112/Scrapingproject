# import time
# import csv
# import os
# import json
# from datetime import datetime, timedelta
# from scrapers.base_scraper import BaseScraper
# from utils.selenium_utils import configure_translation_options
# from utils.selenium_utils import wait_for_element
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# class VCCirclePEScraper(BaseScraper):
#     def __init__(self, headless=True):
#         super().__init__(headless)
#         self.website = "https://www.vccircle.com/deal-type/pe"
#         self.csv_filename = "vccircle_pe_articles.csv"
#         self.progress_file = "vccircle_pe_progress.json"  # Store last scraped URL
#         self.two_months_ago = datetime.now() - timedelta(days=60)

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

#             last_article_old = False

#             while not last_article_old:
#                 try:
#                     wait_for_element(self.driver, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div')

#                     # # Wait for articles to load
#                     # wait_for_element(self.driver, ['//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div'] )
#                 except TimeoutException:
#                     print("Page took too long to load. Stopping.")
#                     break

#                 articles = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div')

#                 for index, article in enumerate(articles):
#                     try:
#                         date_text = article.find_element(By.XPATH, './div/div[2]/div/div').text.strip()
#                         url = article.find_element(By.XPATH, './div/div[2]/h4/a').get_attribute("href")
#                         title = article.find_element(By.XPATH, './div/div[2]/h4').text.strip()
#                         body = article.find_element(By.XPATH, './div/div[2]/p').text.strip()
#                         type_of_news = article.find_element(By.XPATH, './div/div[2]/div/h3/a').text.strip()
#                         source = article.find_element(By.XPATH, './div/div[2]/ul/li/a').text.strip()

#                         formatted_date = self.parse_and_format_date(date_text)
#                         article_date = datetime.strptime(formatted_date, "%d - %m - %Y") if formatted_date else None

#                         if article_date and article_date < self.two_months_ago:
#                             print(f"Stopping: Found an old article from {formatted_date}.")
#                             last_article_old = True
#                             break

#                         writer.writerow([formatted_date, title, body, url, type_of_news, source])
#                         print(f"Saved Article {index+1}: {title} ({formatted_date})")

#                         self.save_progress(url)  # Save progress after each article

#                     except NoSuchElementException:
#                         print(f"Missing data in article {index+1}. Skipping.")
#                         continue

#                 if last_article_old:
#                     break

#                 # Click "Next Page" button
#                 try:
#                     pagination_buttons = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/ul/li/a')

#                     if pagination_buttons:
#                         next_button = pagination_buttons[-1]  # Select last pagination button
#                         self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
#                         time.sleep(3)
#                         self.driver.execute_script("arguments[0].click();", next_button)
#                         print("Clicked 'Next Page' button")
#                         time.sleep(5)
#                     else:
#                         print("\nNo more pages found. Stopping.")
#                         last_article_old = True
#                 except NoSuchElementException:
#                     print("\nNo 'Next Page' button found. Stopping.")
#                     last_article_old = True

#         print(f"\nScraping complete! Data saved to {self.csv_filename}")
#         self.close()



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
# # from utils.save_progress import save_progress
# # from utils.save_progress import load_progress


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


import time
import csv
import json
import os
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapers.base_scraper import BaseScraper
# from utils.db_utils import insert_page_data  # Database insertion (commented out)
from utils.selenium_utils import wait_for_element  # Assuming this is a helper

class VCCirclePEScraper(BaseScraper):
    def __init__(self, headless=True):
        super().__init__(headless)
        self.website = "https://www.vccircle.com/deal-type/pe"
        self.csv_filename = "vccircle_pe_articles.csv"
        self.progress_file = "vccircle_pe_progress.json"  # Store last scraped URL
        self.two_months_ago = datetime.now() - timedelta(days=60)
        self._init_csv()

    def _init_csv(self):
        """Initialize CSV file with headers."""
        with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Title", "Body", "URL", "Type", "Source"])

    def parse_and_format_date(self, date_str):
        """Convert '14 January, 2025' into '14 - 01 - 2025'."""
        try:
            parsed_date = datetime.strptime(date_str, "%d %B, %Y")
            return parsed_date.strftime("%d - %m - %Y")
        except ValueError:
            print(f"⚠ Warning: Could not parse date '{date_str}', skipping article.")
            return None

    def load_progress(self):
        """Load last scraped article URL from the progress file."""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    return data.get("last_scraped_url")
            except (json.JSONDecodeError, FileNotFoundError):
                print("Warning: Progress file is empty or corrupted. Starting from scratch.")
        return None

    def save_progress(self, last_scraped_url):
        """Save last scraped article URL to the progress file."""
        with open(self.progress_file, 'w') as f:
            json.dump({"last_scraped_url": last_scraped_url}, f)

    def open_website(self):
        """Opens the VCCircle PE page."""
        self.driver.get(self.website)
        time.sleep(3)

    def get_article_elements(self):
        """Wait for and return all article elements on the page."""
        try:
            wait_for_element(self.driver, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div')
            articles = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/div[4]/div')
            return articles
        except TimeoutException:
            print("Page took too long to load articles. Stopping.")
            return []

    def process_article(self, article):
        """
        Extract data from a single article element.
        Returns a tuple: (formatted_date, title, body, url, type_of_news, source)
        Returns "STOP" if the article is older than 2 months.
        """
        try:
            date_text = article.find_element(By.XPATH, './div/div[2]/div/div').text.strip()
            url = article.find_element(By.XPATH, './div/div[2]/h4/a').get_attribute("href")
            title = article.find_element(By.XPATH, './div/div[2]/h4').text.strip()
            body = article.find_element(By.XPATH, './div/div[2]/p').text.strip()
            type_of_news = article.find_element(By.XPATH, './div/div[2]/div/h3/a').text.strip()
            source = article.find_element(By.XPATH, './div/div[2]/ul/li/a').text.strip()

            formatted_date = self.parse_and_format_date(date_text)
            if not formatted_date:
                return None
            article_date = datetime.strptime(formatted_date, "%d - %m - %Y")
            if article_date < self.two_months_ago:
                print(f"Stopping: Found an old article from {formatted_date}.")
                return "STOP"
            return (formatted_date, title, body, url, type_of_news, source)
        except NoSuchElementException:
            print("Missing data in an article. Skipping.")
            return None

    def write_article_to_csv(self, article_data):
        """Append article data to the CSV file."""
        with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(article_data)

    def click_next_page(self):
        """Clicks the 'Next Page' button to load more articles."""
        try:
            pagination_buttons = self.driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div/div[2]/div[1]/ul/li/a')
            if pagination_buttons:
                next_button = pagination_buttons[-1]  # Select the last pagination button
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(3)
                self.driver.execute_script("arguments[0].click();", next_button)
                print("Clicked 'Next Page' button.")
                time.sleep(5)
                return True
            else:
                print("No more pages found. Stopping.")
                return False
        except NoSuchElementException:
            print("No 'Next Page' button found. Stopping.")
            return False

    def scrape_articles(self):
        """Scrape articles from the current page and save to CSV."""
        articles = self.get_article_elements()
        if not articles:
            return False

        last_scraped_url = self.load_progress()
        start_index = 0
        # Build list of article links from the current page
        article_links = []
        for article in articles:
            try:
                link = article.find_element(By.XPATH, './div/div[2]/h4/a').get_attribute("href")
                article_links.append((article, link))
            except NoSuchElementException:
                continue

        if last_scraped_url and last_scraped_url in [link for (_, link) in article_links]:
            start_index = [link for (_, link) in article_links].index(last_scraped_url) + 1

        for article, link in article_links[start_index:]:
            result = self.process_article(article)
            if result == "STOP":
                return False
            elif result:
                self.write_article_to_csv(result)
                print(f"Saved article: {result[1]} ({result[0]})")
                self.save_progress(link)
                time.sleep(2)
        return True

    def run(self):
        """Main entry point for the scraper."""
        self.open_website()
        time.sleep(3)
        while True:
            if not self.scrape_articles():
                break
            if not self.click_next_page():
                break
        print("\nScraping complete! Data saved to CSV.")
        self.driver.quit()

if __name__ == '__main__':
    scraper = VCCirclePEScraper(headless=False)
    scraper.run()
