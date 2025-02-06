from datetime import datetime

def parse_article_date(date_text):
    """Parse a date from the string format '%Y-%m-%d %H:%M:%S'."""
    try:
        return datetime.strptime(date_text, "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error parsing date: {e}")
        return None


# selenium_utils.py
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



def click_more_button(driver, xpath, max_clicks=5):
    """Clicks the 'More' button repeatedly to load more content."""
    for _ in range(max_clicks):
        try:
            button = wait_for_element(driver, xpath)
            button.click()
            time.sleep(2)
        except Exception:
            break  # Stop clicking if button is not found

def wait_for_element(driver, xpath, timeout=10):
    """Wait for an element to appear using its XPath."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
