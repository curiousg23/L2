# L2
Coding challenge for L2
- To run this code:
    - Install [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/#Download) (`pip install beautifulsoup4`)
    - Make sure a `brands.csv` file exists if it doesn't already
    - Run `scraper.py` to scrape today's data from Walmart, appending it to the csv file `brands.csv` which contains the scraped data
    - Run `stats.py begin_date end_date` to generate statistics (`begin_date` and `end_date` should be in the form `DD/MM/YYYY`)
- Correlations:
    - There does not appear to be a high correlation between search ranking and reviews, nor search ranking and number of ratings--they were respectively around -0.15 and -0.20
