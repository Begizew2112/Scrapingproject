
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from utils.selenium_utils import configure_translation_options
import time
import os
import json
from datetime import datetime, timedelta

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

class BaseScraper:
    def __init__(self, headless=True, source_lang="zh-CN", target_lang="en"):
        options = Options()
        
        if headless:
            options.add_argument("--headless=new")  # Use the new headless mode

        # Configure translation settings
        configure_translation_options(options, source_lang, target_lang)

        # Additional recommended options
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Initialize WebDriver
        self.driver = webdriver.Chrome(options=options)

    def open_page(self, url):
        """Open a webpage and wait for it to load."""
        self.driver.get(url)
        time.sleep(2)  # Wait for page to load

    def close_driver(self):
        """Closes the WebDriver instance."""
        if self.driver:
            self.driver.quit()

    def wait_for_element(self, xpath, timeout=10):
        """Wait for an element to appear using XPath."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    
    def close_driver(self):
        """Closes the WebDriver instance."""
        if self.driver:
            self.driver.quit()