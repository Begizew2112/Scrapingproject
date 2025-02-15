import os
import json
import csv

def load_progress(progress_file):
    """Load last scraped article URL and page URL from the progress file."""
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                data = json.load(f)
                return data.get("last_scraped_url"), data.get("last_page_url")  # Get both URLs
        except (json.JSONDecodeError, FileNotFoundError):
            print("⚠ Warning: Progress file is empty or corrupted. Starting from scratch.")
            return None, None  # Return None if there's an issue with the file
    return None, None  # Start from the first page and no last scraped URL

def save_progress(last_scraped_url, last_page_url, progress_file):
    """Save last scraped article URL and page URL to progress file."""
    import os
    os.makedirs(os.path.dirname(progress_file), exist_ok=True)  # Ensure the directory exists
    with open(progress_file, 'w') as f:
        json.dump({"last_scraped_url": last_scraped_url, "last_page_url": last_page_url}, f)
        
def _init_csv(self):
    """Initialize CSV file with headers if it doesn't already exist."""
    if not os.path.exists(self.csv_filename):
        with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:  # Open CSV in append mode
            writer = csv.writer(file)
            writer.writerow(["Title", "Source", "Date", "Article Content", "URL"])