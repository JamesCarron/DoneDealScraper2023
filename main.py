import json
import requests
from bs4 import BeautifulSoup
import time
import math

"""
Donedeal search results are 30 per page
https://www.donedeal.ie/cars/Ford/Fiesta?sort=publishdatedesc&start=0
Spotlights will make this a pain in the ass. They can cause duplicates and often ignore search filters

Plan:
Get total number of results -       get_number_of_donedeal_search_page_results()
Load 30 search results                    
    Get all search results in page  get_search_results()
    Get summary attributes of each entry    get_donedeal_result_attribs()
    Delay a time 2s? To prevent being banned. 
        +- random time interval


"""


def get_search_results():
    """
    Returns a list of BS4 objects. One for each search entry

    Example search entry
    ------------------------
    example.html
    Search to get result:
    https://www.donedeal.ie/cars/Ford/Fiesta/Kildare?sort=publishdatedesc&engine_from=1000&engine_to=1000

    Result Page:
    https://www.donedeal.ie/cars-for-sale/151-ford-fiesta-1-0-zetec-ecoboost-100ps/33375779
    """

    # Dummy Code:

    with open("example.html", "r") as file:
        search_result = file.read()

    return [search_result, search_result, search_result]


def parse_donedeal_search_result(search_result: str) -> str:
    """

    Parse the basic summary attributes from a search entry

    Eg from example.html
    :return:
    {
        "title": "151 Ford Fiesta 1.0 Zetec Ecoboost 100PS",
        "price": "€10,950",
        "year": "2015",
        "engine_size": "1.0 Petrol",
        "mileage": "56,000 mi",
        "ad_age": "1 day",
        "location": "Kildare",
        "link": "https://www.donedeal.ie/cars-for-sale/151-ford-fiesta-1-0-zetec-ecoboost-100ps/33375779"
    }
    """

    # Dummy Code:

    parsed_result = """{
        "title": "151 Ford Fiesta 1.0 Zetec Ecoboost 100PS",
        "price": "€10,950",
        "year": "2015",
        "engine_size": "1.0 Petrol",
        "mileage": "56,000 mi",
        "ad_age": "1 day",
        "location": "Kildare",
        "link": "https://www.donedeal.ie/cars-for-sale/151-ford-fiesta-1-0-zetec-ecoboost-100ps/33375779"
    }"""

    return parsed_result


def get_number_of_donedeal_search_results(url: str) -> int:
    """
    Get total number of results returned by search
    """

    # Dummy Code:
    return 1400


def scrape_donedeal_url(
    url: str, results_per_page: int = 30, donedealsortorder: str = "publishdatedesc"
) -> str:
    """
    Takes a donedeal search url and returns a json list containing the basic details of all the cars in that search
    """
    # TODO donedealsortoder should probably be an enum

    results = get_number_of_donedeal_search_results()

    for page in math.ceil(results / results_per_page):
        # I know this can be done in one fstring but I think this is more legible
        page = url + f"sort={donedealsortorder}" + f"&start={page*30:d}"
        search_results = get_search_results(url)
        search_summary_attribs = [
            parse_donedeal_search_result(search_result)
            for search_result in search_results
        ]

        # TODO change this list output to JSON
        return search_summary_attribs


if __name__ == "__main__":
    # Scrape Ford fiesta details
    # TODO fname and url should be passed as command line parameters probably using argparse

    fname = "cars.json"
    url = "https://www.donedeal.ie/cars/Ford/Fiesta"

    cars = scrape_donedeal_url(url)

    # Write to file
    with open(fname, "w", encoding="utf-8") as outfile:
        print("Writing cars to file:", fname)
        json.dump(cars, outfile)
