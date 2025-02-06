# import json
# import os
# import sys
# from scrapers.base_scraper import BaseScraper 
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# def load_progress(self):
#     """Load last scraped article URL from the progress file."""
#     if os.path.exists(self.progress_file):
#         with open(self.progress_file, 'r') as f:
#             data = json.load(f)
#             return data.get("last_scraped_url")
#     return None

# def save_progress(self, last_scraped_url):
#     """Save last scraped article URL to progress file."""
#     with open(self.progress_file, 'w') as f:
#         json.dump({"last_scraped_url": last_scraped_url}, f)