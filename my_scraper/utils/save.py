import json
import os
from selenium.webdriver.common.by import By

def load_progress(progress_file):
    """Load the last progress (page number and article index) from the progress file."""
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            try:
                data = json.load(f)
                return data.get("page_number", 1), data.get("article_index", 1)  # Default to page 1, article 1
            except json.JSONDecodeError:
                print("⚠ Warning: Progress file is corrupted. Starting from scratch.")
    return 1, 1  # Start from the first page, first article

def save_progress(progress_file, page_number, article_index):
    """Save the current progress (page number and article index) to the progress file."""
    with open(progress_file, 'w') as f:
        json.dump({"page_number": page_number, "article_index": article_index}, f)

def get_total_articles_on_page(driver):
    """Returns the total number of articles on the current page dynamically."""
    try:
        articles = driver.find_elements(By.XPATH, '//*[@id="lists"]/li')
        return len(articles)
    except Exception as e:
        print(f"Error finding articles: {e}")
        return 0
