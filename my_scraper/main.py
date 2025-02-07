from scrapers.dealstreet_venture_capital import DealStreetScraper
from scrapers.private_equity_scraper import PrivateEquityScraper
from scrapers.fromgeek_scraper import FromGeekScraper
from scrapers.techstars_scraper import TechStarsScraper
from scrapers.vccircle_pe_scraper import VCCirclePEScraper  # New scraper added
from scrapers.vccircle_venture_capital import VCCirclesVentureCapital# New scraper added
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Choose which scraper to run
SCRAPER_TO_RUN = "fromgeek"  # Change as needed

if __name__ == "__main__":
    if SCRAPER_TO_RUN == "dealstreet":
        scraper = DealStreetScraper(headless=True)
    elif SCRAPER_TO_RUN == "private_equity":
        scraper = PrivateEquityScraper(headless=True)
    elif SCRAPER_TO_RUN == "fromgeek":
        scraper = FromGeekScraper(headless= True)
    elif SCRAPER_TO_RUN == "techstars":
        scraper = TechStarsScraper(headless=False)
    elif SCRAPER_TO_RUN == "vccircle_pe":  # New option for VCCircle PE
        scraper = VCCirclePEScraper(headless=True)
    elif SCRAPER_TO_RUN == "vccircle_capital":  # New option for VCCircle PE
        scraper = VCCirclesVentureCapital(headless=True)
    else:
        raise ValueError("Invalid scraper selection!")
    # Start scraping the selected scraper
    scraper.scrape_articles()
    #scraper.run()


#from scrapers.fromgeek_scraper import FromGeekScraper
# # Scraper for French to English
# scraper = FromGeekScraper(headless=False)
# scraper.scrape()

# # Scraper for German to English
# scraper_german = FromGeekScraper(headless=False, source_lang="de", target_lang="en")
# scraper_german.scrape()
