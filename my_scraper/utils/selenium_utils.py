# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from selenium import webdriver

# def configure_translation_options(driver_options, source_lang="zh-CN", target_lang="en"):
#     """
#     Configures the Chrome WebDriver to automatically translate a given language to another.
    
#     Parameters:
#     - driver_options: ChromeOptions object
#     - source_lang: The language to translate from (e.g., "fr" for French, "de" for German)
#     - target_lang: The target language (default is "en" for English)
#     """
#     driver_options.add_experimental_option(
#         "prefs", {"translate_whitelists": {source_lang: target_lang}, "translate": {"enabled": "true"}}
#     )

# def wait_for_element(driver, xpath, timeout=10):
#     """Wait for an element to appear using its XPath."""
#     return WebDriverWait(driver, timeout).until(
#         EC.presence_of_element_located((By.XPATH, xpath))
#     )

# def click_more_button(driver, xpath, max_clicks=5):
#     """Clicks the 'More' button repeatedly to load more content."""
#     for _ in range(max_clicks):
#         try:
#             button = wait_for_element(driver, xpath)
#             button.click()
#             time.sleep(2)
#         except Exception:
#             break  # Stop clicking if button is not found
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver

import os
import json
import csv
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

def create_selenium_driver(headless=True):
    """
    Creates a Selenium WebDriver instance with a random User-Agent and optional headless mode.

    :param headless: Boolean to determine if the browser should run in headless mode. Default is True.
    :return: Selenium WebDriver instance.
    """
    # Set up fake User-Agent
    ua = UserAgent()
    
    # Set up Chrome options
    options = Options()
    options.add_argument(f"user-agent={ua.random}")  # Fake User-Agent

    if headless:
        options.add_argument("--headless")  # Optional: Run in headless mode
    
    # Initialize WebDriver
    driver = webdriver.Chrome(options=options)

    return driver


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
