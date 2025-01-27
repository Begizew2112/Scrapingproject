from scrapers.dealstreet_scraper import DealStreetScraper
from scrapers.private_equity_scraper import PrivateEquityScraper
from scrapers.fromgeek_scraper import FromGeekScraper
from scrapers.techstars_scraper import TechStarsScraper  # New scraper added

# Choose which scraper to run
SCRAPER_TO_RUN = "techstars"  # Change to "dealstreet", "private_equity", "fromgeek", or "techstars" as needed

if __name__ == "__main__":
    if SCRAPER_TO_RUN == "dealstreet":
        scraper = DealStreetScraper(headless=True)
    elif SCRAPER_TO_RUN == "private_equity":
        scraper = PrivateEquityScraper(headless=True)
    elif SCRAPER_TO_RUN == "fromgeek":
        scraper = FromGeekScraper(headless=True)
    elif SCRAPER_TO_RUN == "techstars":  # New option for TechStars
        scraper = TechStarsScraper(headless=True)
    else:
        raise ValueError("Invalid scraper selection!")

    scraper.scrape_articles()


#from scrapers.fromgeek_scraper import FromGeekScraper

# # Scraper for French to English
# scraper = FromGeekScraper(headless=False)
# scraper.scrape()

# # Scraper for German to English
# scraper_german = FromGeekScraper(headless=False, source_lang="de", target_lang="en")
# scraper_german.scrape()
