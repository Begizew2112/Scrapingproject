# Sources Scraping Project

A web scraping project built with Python and Selenium to collect venture capital and startup news from various sources.

## Features

- Scrapes venture capital and startup news articles
- Automatic translation to English
- Saves data to CSV files
- Configurable date range for article collection
- Extracts article titles, dates, view counts, sources, and content

## Prerequisites

- Python 3.12+
- Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/valueize/sources-scraper
cd sources-scraper
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Start with FromGeek scraper:

```bash
jupyter notebook news_scraper/news_scraper/spiders/website1/fromgeek.ipynb
```

2. Run DealStreetAsia scraper:

```bash
jupyter notebook news_scraper/news_scraper/spiders/website2/dealstreate_asia.ipynb
```

The scraped data will be saved to CSV files in the respective directories.

## Project Structure

```
scrapingproject/
├── LICENSE
├── README.md
├── requirements.txt
└── news_scraper/
    └── news_scraper/
        └── spiders/
            ├── website1/
            │   ├── fromgeek.ipynb
            │   └── fromgeekhtml.ipynb
            └── website2/
                ├── dealstreate_asia.ipynb
                └── dealstreat_html.ipynb
```

## Configuration

- To modify the date range for article collection, adjust the `timedelta` parameter in the scraping scripts
- Chrome translation settings can be configured in the `ChromeOptions` section
- CSV output filenames and locations can be customized in the scripts

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

- If ChromeDriver fails to start, ensure your Chrome browser and ChromeDriver versions match
- For translation issues, try increasing the `time.sleep()` duration to allow more time for translation
- If scraping fails, check the website's structure hasn't changed and update the XPath selectors accordingly
