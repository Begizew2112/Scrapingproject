import csv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def save_to_csv(filename, data):
    """Save data to CSV file."""
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

