
####################* Dependencies ####################
import datetime
import os
import re
from datetime import datetime
from threading import Thread
from time import sleep
from tkinter import TRUE
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import pandas as pd

# Advanced, custom element locator function
from selenium_functions import custom_find_my_element

####################*    START    ####################

# variables
DELAY = 3
SLEEP_TIME_VARIABLE = 1
STOP_CONDITION = False
boliga_url = "https://www.boliga.dk/resultat?propertyType=1,2,5,6,9&sort=daysForSale-d"

# Lists to store extracted data
prices = []
addresses = []
m2_sizes = []
times_on_market = []
num_rooms = []
energy_classes = []
build_years = []
property_sizes = []

# browser settings
options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('log-level=3')

# define find_my_element
def find_my_element(driver, xpath):
    return custom_find_my_element(driver, xpath, DELAY = DELAY)

# define class for the bot
class boliga_bot():
    def load_browser(self):
        self.driver = webdriver.Chrome(service=Service(),options=options)
        self.driver.maximize_window()
        self.driver.get('https://www.boliga.dk/')

    def load_search_page(self):

        #? This function demonstrates how to access the correct page without using the URL below
        # https://www.boliga.dk/resultat?propertyType=1,2,5,6&sort=daysForSale-d

        # Remove cookie pop-up
        find_my_element(self.driver, "//*[contains(text(), 'Tillad alle')]").click()
        # load search page
        list_btn_xpath = "//button[contains(@class, 'app-button') and contains(@class, 'app-search-btn') and contains(@class, 'primary') and .//span[contains(text(), 'Liste')]]"
        find_my_element(self.driver, list_btn_xpath).click()
        sleep(2)
        # set options
        udvidet_soeg_xpath = "//div[@data-gtm='filter_more_filters' and contains(@class, 'advanced-filter-btn')]"
        find_my_element(self.driver, udvidet_soeg_xpath).click()
        # define relevant property types
        relevant_types = ["Villa", "Villalejlighed", "Landejendom", "Rækkehus", "Andelsbolig"]
        # select property types in opetions
        for a_type in relevant_types:
            ul_element_xpath = '//div[contains(@class, "type-house-list-block")]/ul'
            ul_element = find_my_element(self.driver, ul_element_xpath)
            li_elements = ul_element.find_elements(By.XPATH, './li')
            for li in li_elements:
                if a_type in li.text:
                    li.click()
                    break
        sleep(2)
        # click search
        print("a")
        try:
            # first click scrolls down to element, does not click
            find_my_element(self.driver, '//button[contains(@class, "app-button") and contains(@class, "primary") and contains(@class, "font-medium")]').click()
        except:
            # this click clicks
            find_my_element(self.driver, '//button[contains(@class, "app-button") and contains(@class, "primary") and contains(@class, "font-medium")]').click()
        print("b")
        # click order by: oldest first.
        find_my_element(self.driver, '//button[@class="order"]').click()
        sleep(3)
        assert self.driver.current_url == boliga_url

    def extract_data_from_current_page(self):
        print("extracting")
        sleep(3)
        housing_list_results_container = find_my_element(bot.driver, './/div[contains(@class, "housing-list-results")]')
        housing_list_items = housing_list_results_container.find_elements(By.XPATH, './/app-housing-list-item')
        
        for item in housing_list_items:
            # Extract data from each item
            price_element = item.find_element(By.XPATH, './/div[contains(text(), "kr.")]')
            two_last = price_element.text.split()[-2:]
            price = two_last[0]
            prices.append(price)
            # Address and Zip
            address_element = item.find_element(By.XPATH, ".//div[contains(@class, 'secondary-value')]")
            address_parts = [elem.text for elem in address_element.find_elements(By.XPATH, ".//span")]
            address = ', '.join(address_parts)
            addresses.append(address)
            try:
                # Details
                details_div = item.find_element(By.XPATH, ".//div[contains(@class, 'house-details-blocks')]")
                rooms = details_div.find_element(By.XPATH, "./div[1]").text
                m2_size = details_div.find_element(By.XPATH, "./div[2]").text
                energy_class = details_div.find_element(By.XPATH, "./div[3]").text
                build_year = details_div.find_element(By.XPATH, "./div[4]").text
                property_size = details_div.find_element(By.XPATH, "./div[5]").text
                # time_on_market_element = item.find_element(By.XPATH, ".//app-property-label/following-sibling::app-tooltip[1]/p")
                # time_on_market = time_on_market_element.text
                print(f"Address: {address} | Price: {price}\n rooms{rooms}m2size{m2_size}eclass{energy_class}byear{build_year}psize{property_size}\n\n")
                num_rooms.append(rooms)
                m2_sizes.append(m2_size)
                energy_classes.append(energy_class)
                build_years.append(build_year)
                property_sizes.append(property_size)
            except:
                print(f"ERROR FOR {address} - {price_element}")
                num_rooms.append('not found')
                m2_sizes.append('not found')
                energy_classes.append('not found')
                build_years.append('not found')
                property_sizes.append('not found')

    def number_of_pages(self):
        number_of_pages_element = find_my_element(bot.driver, "//div[@class='jump-to-page ng-star-inserted']/a[@class='page-button']")
        return int(number_of_pages_element.text)

global bot
bot = boliga_bot()


def save_data_to_csv(addresses, prices, m2_sizes, property_sizes, num_rooms, energy_classes, build_years):
    """
    Convert the extracted data to a Pandas DataFrame and save it to a CSV file.
    If the file exists, append the data. Otherwise, create a new file.
    """
    df = pd.DataFrame({
        'Address': addresses,
        'Price': prices,
        'Size (m2)': m2_sizes,
        'Property size': property_sizes,
        'Number of rooms': num_rooms,
        'Energy class': energy_classes,
        'Build year': build_years,
    })
    
    # Check if the CSV file exists
    if os.path.exists("housing_data.csv"):
        df.to_csv("housing_data.csv", mode='a', header=False, encoding='utf-8-sig', index=False, sep=';')
    else:
        df.to_csv("housing_data.csv", index=False, encoding='utf-8-sig', sep=';')


if __name__ in '__main__':
    # load the web-scraper
    bot.load_browser()
    bot.load_search_page()
    bot.extract_data_from_current_page() #? This should only be used if skip_pages is zero
    skip_pages = 0 # 0
    for page in range(bot.number_of_pages()):
        page_no = skip_pages + page + 2 # start with + 2
        print(f"Getting data from {page_no}")
        bot.driver.get(boliga_url + f"&page={page_no}")
        sleep(1)
        bot.extract_data_from_current_page()
        save_data_to_csv(addresses, prices, m2_sizes, property_sizes, num_rooms, energy_classes, build_years)  # Call the function here
        



"""
housing_list_results_container = find_my_element(bot.driver, './/div[contains(@class, "housing-list-results")]')
housing_list_items = housing_list_results_container.find_elements(By.XPATH, './/app-housing-list-item')
for i, item in enumerate(housing_list_items):
     print(f"Item {i + 1} content:\n{item.text}\n{'-'*50}") 
     print(f"Item {i + 1} HTML:\n{item.get_attribute('outerHTML')}\n{'-'*50}")
     break

item = housing_list_items[0]
"""




