import os
import json
#from scrapers.base_scraper import BaseScraper
def load_progress(progress_file):
    """Load the last scraped article URL from the progress file."""
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r') as f:
                data = json.load(f)
                return data.get("last_scraped_url")
        except (json.JSONDecodeError, FileNotFoundError):
            print("⚠ Warning: Progress file is empty or corrupted. Starting from scratch.")
            return None
    return None

def save_progress(progress_file, last_scraped_url):
    """Save the last scraped article URL to the progress file."""
    with open(progress_file, 'w') as f:
        json.dump({"last_scraped_url": last_scraped_url}, f)
