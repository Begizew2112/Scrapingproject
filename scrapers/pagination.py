from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

class FromGeekScraper:
    def __init__(self):
        # Initialize the WebDriver with the option to open a visible browser window
        options = Options()
        # options.add_argument("--headless")  # Comment out or remove this line
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "https://www.fromgeek.com/vc/"

    def click_next_page(self):
        """Click 'Next Page' button to continue pagination."""
        try:
            next_buttons = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[1]/div/div/div[2]/div[2]/a')

            if next_buttons:
                next_button = next_buttons[-1]  # Select the last button dynamically
                print(f"Clicking Next Page button: {next_button.text}")  

                # Check if the button is visible and enabled
                if next_button.is_displayed() and next_button.is_enabled():
                    self.driver.execute_script("arguments[0].click();", next_button)  # Click using JavaScript
                    time.sleep(5)  # Wait for page load
                    return True

            print("No 'Next Page' button found, stopping pagination.")
            return False

        except Exception as e:
            print(f"Error clicking 'Next Page' button: {e}")
            return False

    def open_page(self, url):
        """Open the base URL of the website."""
        self.driver.get(url)

    def close(self):
        """Close the browser."""
        self.driver.quit()

# Run the pagination test
scraper = FromGeekScraper()
scraper.open_page(scraper.base_url)
time.sleep(5)  # Wait for the page to load initially

page_number = 1
while True:
    print(f"Scraping page {page_number}...")

    # After scraping all articles on the page, check if pagination should continue
    if not scraper.click_next_page():
        break

    page_number += 1

print("Pagination completed.")
scraper.close()
