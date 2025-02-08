import time
import csv
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scrapers.base_scraper import BaseScraper
import json
from utils.db_utils import insert_page_data
import sys
import os
from utils.date_utils import parse_article_date
from utils.csv_utils import save_to_csv 
from utils.save import load_progress,save_progress
from utils.save import get_total_articles_on_page
class FromGeekScraper(BaseScraper):
    def __init__(self, headless=False, source_lang="zh-CN", target_lang="en"):
        super().__init__(headless=headless, source_lang=source_lang, target_lang=target_lang)
        self.base_url = "https://www.fromgeek.com/vc/"
        self.csv_filename = "fromgeek_scraped_articles.csv"
        self.progress_file = "fromgeek_scraped.json" 
        self.two_months_ago = datetime.now() - timedelta(days=60)
        self.data = []
        self.page_number, self.article_index = load_progress(self.progress_file)

        # Initialize CSV file with headers
        with open(self.csv_filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Article URL", "Title", "Date", "View", "Source", "Content"])

        # Load last progress
        self.page_number, self.article_index = load_progress(self.progress_file)

    # def load_progress(self):
    #     """Load the last progress (page number and article index) from the progress file."""
    #     if os.path.exists(self.progress_file):
    #         with open(self.progress_file, 'r') as f:
    #             data = json.load(f)
    #             return data.get("page_number", 1), data.get("article_index", 1)  # Default to page 1, article 1
    #     return 1, 1  # Start from the first page, first article

    # def save_progress(self, page_number, article_index):
    #     """Save the current progress (page number and article index) to the progress file."""
    #     with open(self.progress_file, 'w') as f:
    #         json.dump({"page_number": page_number, "article_index": article_index}, f)

    # def get_total_articles_on_page(self):
    #     """Returns the total number of articles on the current page dynamically."""
    #     try:
    #         articles = self.driver.find_elements(By.XPATH, '//*[@id="lists"]/li')
    #         return len(articles)
    #     except Exception as e:
    #         print(f"Error finding articles: {e}")
    #         return 0

    def scrape_articles(self):
        self.open_page(self.base_url)
        time.sleep(5)

        page_number = self.page_number  # Resume from saved page number

        try:
            while True:
                print(f"Scraping page {page_number}...")
                total_articles = get_total_articles_on_page(self.driver)
                i = self.article_index  # Resume from the saved article index

                while i <= total_articles:
                    try:
                        article_link = self.driver.find_element(By.XPATH, f'//*[@id="lists"]/li[{i}]/div[1]/h4/a')
                        article_url = article_link.get_attribute("href")
                        article_link.click()
                        time.sleep(2.5)

                        date_text = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[2]').text
                        article_date = parse_article_date(date_text)

                        if article_date and article_date < self.two_months_ago:
                            print(f"Reached an article older than 2 months ({article_date}), stopping...")
                            return

                        title = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/h1').text
                        view = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[1]').text
                        source = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/ul/li[3]').text
                        content = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/article/p[1]').text             

                        self.data.append([article_url, title, article_date.strftime('%Y-%m-%d %H:%M:%S'), view, source, content])
                        save_to_csv(self.csv_filename, self.data)

                        print(f"Scraped: {title} | Date: {article_date}")
                        self.driver.back()
                        time.sleep(3)

                        # Save progress after each successful article
                        save_progress(self.progress_file, self.page_number, self.article_index)

                        i += 1  # Move to the next article
                    except Exception as e:
                        print(f"Finished articles on this page, moving to next page.")
                        time.sleep(6) 
                        break  # Move to the next page

                """Click the 'Next Page' button and return True if successful."""
                if not self.click_next_page():
                    break

                page_number += 1
                #self.save_progress(page_number, 1)  # Reset article index to 1 for the next page
                save_progress(self.progress_file, self.page_number, self.article_index)
                time.sleep(5)
       
        
        finally:
            self.close()  # Ensures the driver is closed properly


    def click_next_page(self):
        """Click the 'Next Page' button and return True if successful."""
        try:
            next_buttons = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[1]/div/div/div[2]/div[2]/a')
            if next_buttons:
                next_button = next_buttons[-1]
                if next_button.is_displayed() and next_button.is_enabled():
                    print(f"Clicking Next Page button: {next_button.text}")
                    self.driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)
                    return True
            print("No 'Next Page' button found, stopping pagination.")
            return False
        except Exception as e:
            print(f"Error clicking 'Next Page' button: {e}")
            return False

    def close(self):
        """Close the browser driver."""
        self.driver.quit()

# if __name__ == "__main__":
#     scraper = FromGeekScraper()
#     scraper.open_page(scraper.base_url)
#     scraper.scrape_articles()
#     print("Scraping completed.")