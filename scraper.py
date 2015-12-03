from bs4 import BeautifulSoup as bs
import requests
import time
import re
import csv

def scrape_page(soup, itms_offset, brand_list, data, date, term):
    """ Scrapes a page for all the items, taking those with the relevant brand
    name and identifying the number of reviews, rating, and position in the
    search results"""

    for idx, a in enumerate(soup.findAll('div', {'class': 'js-tile-landscape'})):
        # grab title of the item
        title_tag = a.find('a', {'class': 'js-product-title'})
        title = ''.join(title_tag.findAll(text=True))

        # check if the item belongs to one of the specified brands
        searched_brand = False
        which_brand = ""
        for brand in brand_list:
            if brand.lower() in title.lower():
                searched_brand = True
                which_brand = brand
                break

        if searched_brand:
            # grab the rating of the item, put -1 if it doesn't exist
            stars_tag = a.find('span', {'class': 'js-reviews'})
            if stars_tag is not None:
                ratings_tag = stars_tag.find('span', {'class': 'visuallyhidden'})
                ratings_str = ''.join(ratings_tag.findAll(text=True))
                rating = float(ratings_str.split(' ')[0])
            else:
                rating = -1.0

            # grab the number of reviews of the item, put -1 if it doesn't exist
            reviews_tag = a.find('span', {'class': 'stars-reviews'})
            if reviews_tag is not None:
                reviews_str = ''.join(reviews_tag.findAll(text=True))
                reviews_str = reviews_str.replace(',','')
                num_reviews = re.findall('\d+', reviews_str)
                num_reviews = int(num_reviews[0])
            else:
                num_reviews = -1

            # insert a data point into the appropriate brand, a tuple of the
            # brand name, search term, rating, number of reviews, position, and
            # date of search
            data[which_brand].append((which_brand, term, rating, num_reviews, itms_offset+idx, date))

def scrape_script():
    base_url = "http://www.walmart.com"
    search_terms = ["cereal", "cold cereal"]
    brand_list = ["Cheerios", "Kashi", "Kellogg\'s", "Post"]
    cur_date = time.strftime("%d/%m/%Y")

    my_dat = dict()
    for brand in brand_list:
        my_dat[brand] = []

    for term in search_terms:
        url = base_url + "/search/?query=" + term
        html = requests.get(url)
        soup = bs(html.content, "html.parser")

        # get the total number of search results
        itms_tag = soup.find('div',{'class': 'result-summary-container'})
        itms_str = ''.join(map(str, itms_tag.contents))
        itms_str = itms_str.replace(',','')
        itms_arr = re.findall('\d+', itms_str)
        num_itms = int(itms_arr[1])
        offset_num = int(itms_arr[0])
        itms_offset = 1

        # get href to next page, if it exists
        next_link = soup.find('a', {'class': 'paginator-btn-next'})
        if next_link is not None:
            next_url = next_link['href']
        else:
            next_url = None

        counter = 1
        print "scraping page %d for search term %s" % (counter, term)
        scrape_page(soup, itms_offset, brand_list, my_dat, cur_date, term)

        while next_url is not None:
            counter += 1
            url = base_url + "/search/" + next_url
            html = requests.get(url)
            soup = bs(html.content, "html.parser")

            itms_offset += offset_num

            next_link = soup.find('a', {'class': 'paginator-btn-next'})
            if next_link is not None:
                next_url = next_link['href']
            else:
                next_url = None
            print "scraping page %d for search term %s" % (counter, term)
            scrape_page(soup, itms_offset, brand_list, my_dat, cur_date, term)

    with open('brands.csv', 'wb') as csvfile:
        brandwriter = csv.writer(csvfile, delimiter=',')
        for brand in brand_list:
            for data_pt in my_dat[brand]:
                brandwriter.writerow(data_pt)

scrape_script()
