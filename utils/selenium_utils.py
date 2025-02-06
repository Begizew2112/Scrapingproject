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

import csv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

