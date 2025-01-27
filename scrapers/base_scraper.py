from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.selenium_utils import configure_translation_options  # Import the translation function

class BaseScraper:
    def __init__(self, headless=True, source_lang="zh-CN", target_lang="en"):
        options = Options()
        if headless:
            options.add_argument("--headless")

        # Configure Chrome to automatically translate pages
        configure_translation_options(options, source_lang, target_lang)

        # Use the manually downloaded ChromeDriver
        chromedriver_path = "C:\\chromedriver-win64\\chromedriver.exe"  # Update path
        self.service = Service(chromedriver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)

    def open_page(self, url):
        """Open a webpage and wait for it to load."""
        self.driver.get(url)
        time.sleep(2)

    def wait_for_element(self, xpath, timeout=10):
        """Wait for an element to appear using XPath."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def scroll_down(self, scrolls=3):
        """Scrolls down the page multiple times."""
        for _ in range(scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

    def close(self):
        """Closes the browser session."""
        self.driver.quit()
