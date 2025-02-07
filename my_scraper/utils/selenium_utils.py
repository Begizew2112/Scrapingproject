import csv
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
#from scrapers.base_scraper import BaseScraper
# from fake_useragent import UserAgent

# #create fault api adress to drease banning from the website
# def create_selenium_driver(headless=True):
#     """
#     Creates a Selenium WebDriver instance with a random User-Agent and optional headless mode.

#     :param headless: Boolean to determine if the browser should run in headless mode. Default is True.
#     :return: Selenium WebDriver instance.
#     """
#     # Set up fake User-Agent
#     ua = UserAgent()
    
#     # Set up Chrome options
#     options = Options()
#     options.add_argument(f"user-agent={ua.random}")  # Fake User-Agent

#     if headless:
#         options.add_argument("--headless")  # Optional: Run in headless mode
    
#     # Initialize WebDriver
#     driver = webdriver.Chrome(options=options)

#     return driver


def configure_translation_options(driver_options, source_lang="zh-CN", target_lang="en"):
    """
    Configures Chrome to automatically translate a given language to another.
    """
    driver_options.add_experimental_option(
        "prefs", {
            "translate_whitelists": {source_lang: target_lang}, 
            "translate": {"enabled": True}
        }
    )
def wait_for_element(driver, xpath, timeout=10):
    """Wait for an element to appear using its XPath."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

def open_website(self):
    """Opens the DealStreetAsia Private Equity page."""
    self.driver.get(self.base_url)
    time.sleep(5)
def parse_and_format_date(date_str):
    """Parses and reformats the date from the article."""
    try:
        return datetime.strptime(date_str, "%d %B, %Y").strftime("%d ,%m, %Y")
    except ValueError:
        print(f"⚠ Warning: Could not parse date '{date_str}', skipping article.")
        return None 



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
        
def click_more_button(driver):
    """Clicks the 'More' button to load additional articles."""
    try:
        more_button = driver.find_element(By.XPATH, '//*[@id="archive-wrapper"]/div[5]/div/button')
        driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", more_button)
        time.sleep(5)
        return True
    except (NoSuchElementException, ElementClickInterceptedException):
        print("No 'More' button found or can't be clicked. Stopping.")
        return False
