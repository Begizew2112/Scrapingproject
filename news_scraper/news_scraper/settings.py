# Increase the delay to wait for the language to switch
DOWNLOAD_DELAY = 5  # Wait 5 seconds between requests
RANDOMIZE_DOWNLOAD_DELAY = True  # Random delay to avoid bot detection

# AutoThrottle settings to handle delays dynamically
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5  # Start with a delay of 5 seconds
AUTOTHROTTLE_MAX_DELAY = 10  # Maximum delay of 10 seconds
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Avoid multiple requests at once
BOT_NAME = 'news_scraper'

SPIDER_MODULES = ['news_scraper.spiders']
NEWSPIDER_MODULE = 'news_scraper.spiders'
