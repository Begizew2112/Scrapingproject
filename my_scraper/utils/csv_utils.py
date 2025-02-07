import csv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv
import os
def save_to_csv(filename, data):
    """Save data to CSV file."""
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def init_csv(csv_filename):
    """Initialize CSV file with headers if it doesn't already exist."""
    if not os.path.exists(csv_filename):
        with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:  # Open CSV in append mode
            writer = csv.writer(file)
            writer.writerow(["Title", "Source", "Date", "Article Content", "URL"])
