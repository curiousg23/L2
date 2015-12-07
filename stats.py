import sys
import csv
import math
from datetime import datetime


def percent_search_results(begin_date, end_date, brands, data):
    """Takes a begin and end date, in the forms DD/MM/YYYY, and a list of
    brands, and returns a dictionary where the value for each brand is the
    percentage of search results that it owns."""
    num_results = dict()
    for brand in brands:
        num_results[brand] = 0
    total_results = 0

    begin_date = datetime.strptime(begin_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")

    for brand in brands:
        for tup in data[brand]:
            if begin_date <= datetime.strptime(tup[5], "%d/%m/%Y") <= end_date:
                num_results[brand] += 1
                total_results += 1.0
    for brand in brands:
        num_results[brand] = 100*num_results[brand]/total_results

    return num_results

def top_three_results(begin_date, end_date, brands, data):
    """Takes a begin and end date, in the forms DD/MM/YYYY, and a list of brands,
    and returns a dictionary where the value for each brand is the percentage of
    the top 3 search results it owns."""
    num_results = dict()
    for brand in brands:
        num_results[brand] = 0
    total_results = 0

    begin_date = datetime.strptime(begin_date, "%d/%m/%Y")
    end_date = datetime.strptime(end_date, "%d/%m/%Y")

    for brand in brands:
        for tup in data[brand]:
            if begin_date <= datetime.strptime(tup[5], "%d/%m/%Y") <= end_date and int(tup[4]) < 4:
                num_results[brand] += 1
                total_results += 1.0
    for brand in brands:
        num_results[brand] = 100*num_results[brand]/total_results

    return num_results

def check_correlation(X, Y):
    """Calculate the correlation between two arrays containing the values of
    nonnegative discrete random variables X and Y."""
    # calculate mean and standard deviation for X and Y
    mean_X = sum(X)/float(len(X))
    mean_Y = sum(Y)/float(len(Y))
    std_X = math.sqrt(sum( [(x-mean_X)**2 for x in X] )/len(X))
    std_Y = math.sqrt(sum( [(y-mean_Y)**2 for y in Y] )/len(Y))
    # calculate covariance
    cov = 0
    for idx, x in enumerate(X):
        a = x - mean_X
        b = Y[idx] - mean_Y
        cov += a*b/len(X)
    # return correlation
    return cov/(std_X*std_Y)

def generate_stats(begin_date, end_date):
    """Generates statistics for brands from a given begin date to an end date,
    where begin and end dates have the form DD/MM/YYYY"""
    brand_list = ["Cheerios", "Kashi", "Kellogg\'s", "Post"]
    my_dat = dict()
    all_ranks = []
    all_ratings = []
    all_reviews = []

    for brand in brand_list:
        my_dat[brand] = []
    with open('brands.csv') as csvfile:
        brandsreader = csv.reader(csvfile)
        for idx, row in enumerate(brandsreader):
            if idx == 0:
                continue
            brand_name = row[0]
            my_dat[brand_name].append(tuple(row))
            if float(row[2]) > 0:
                all_ranks.append(int(row[4]))
                all_ratings.append(float(row[2]))
                all_reviews.append(int(row[3]))

    print "Percentage of search results owned by each brand: "
    print percent_search_results(begin_date, end_date, brand_list, my_dat)
    print "\nPercentage of top 3 search results owned by each brand: "
    print top_three_results(begin_date, end_date, brand_list, my_dat)
    print "\nCorrelation between number of reviews and search ranking: "
    print check_correlation(all_reviews, all_ranks)
    print "\nCorrelation between ratings and search ranking: "
    print check_correlation(all_ratings, all_ranks)

def main(argv):
    if len(argv) != 2:
        print "Incorrect number of arguments. Please provide a begin and end date, in the form DD/MM/YYYY"
    else:
        generate_stats(str(argv[0]), str(argv[1]))

if __name__ == "__main__":
    main(sys.argv[1:])
