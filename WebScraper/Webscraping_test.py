
################################ Packages #################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep, time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests
from bs4 import BeautifulSoup

################################ START #################################

# browser settings
options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument('log-level=3')

url = "https://home.dk/"

class home_bot():

    def initialize_driver(self):
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.driver.maximize_window()
        self.driver.get(url)
        global wait, DELAY
        DELAY = 3
        wait = WebDriverWait(self.driver, DELAY)

    # Accept cookies
    def accept_cookies(self):
        cookie_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'coi-banner__accept')))
        cookie_button.click()

    # Navigate to the list containing properties for sale
    def navigate_to_property_list(self):
        menu_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'handle-text')))
        menu_button.click()
        sog_bolig_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Søg bolig')))
        sog_bolig_button.click()

    # Filter the list to only contain necessary elements
    def filter_properties(self):
        label_leje = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(),'Boliger til leje*')]")))
        label_leje.click()

        #list of desired property types
        ejendomstype_click = ["Villa", "Rækkehus", "Lejlighed", "Landejendom", "Andelsbolig", "Villalejlighed"]
        
        #Loop through each labeltext and click on the corresponding label
        for ejendom in ejendomstype_click:
            ejendom_element = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[@id='estate-type']//label[contains(text(), '{ejendom}')]")))
            ejendom_element.click()

        sleep(2)
        WebDriverWait(self.driver, DELAY).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='selectric']//p[@class='label' and text()='Sorter']"))).click()
        WebDriverWait(self.driver, DELAY).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='selectric-items']//li[text()='Liggetid (ældste først )']"))).click()

    # Check if the "boliger" count has changed from "0 boliger"
    def wait_for_non_zero_boliger_count(self, timeout=60):  # Added timeout parameter
        start_time = time()
        while time() - start_time < timeout:
            try:
                boliger_element = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[@class='xl-heading']")))
                boliger_count = boliger_element.text.split()[0]  # Grab the first part of "n boliger"
                if int(boliger_count) > 0:  # Check if the count is greater than zero
                    return True
            except Exception as e:
                print(f"An error occurred while waiting for non-zero boliger count: {e}")

            sleep(0.5)
        raise Exception("Timeout while waiting for non-zero boliger count")


global bot
bot = home_bot()


if __name__ in '__main__':
    bot.initialize_driver()
    
    bot.accept_cookies()
    bot.navigate_to_property_list()
    # bot.wait_for_non_zero_boliger_count()  # Wait here until the count is non-zero
    bot.sleep(5)
    bot.filter_properties()


###! DEV:

gallery = WebDriverWait(bot.driver, DELAY).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="result-gallery"]')))
temp = gallery.find_elements(By.XPATH, './div')
items = temp[1].find_elements(By.XPATH, './section')
item0 = items[0]


item0.find_element(By.XPATH, ".//span[@ng-if='result.ejendomstypePrimaerNicename']")

for item in items:
    print("streetAddress " + item.find_element(By.XPATH, ".//span[@itemprop='address']/b[@itemprop='streetAddress']").text)
    print("price " + item.find_element(By.XPATH, ".//span[@itemprop='price']").text)
    # villa type item.find_element(By.XPATH, ".//span[@ng-if='result.ejendomstypePrimaerNicename']")

################################ BeautifulSoup #################################
"""
sleep(5)

current_url = driver.current_url

print(current_url)

driver.quit()  # Use quit() to close the browser.
# URL (Assuming you have it defined somewhere)

headers = {
    'name': 'Mert Cetinkaya',
    'email': 'mwg934@alumni.ku.dk',
    "purpose": "examproject where we analyze housing prices"
}
response = requests.get(current_url, headers=headers)

# Parse data with BeautifulSoup
soup = BeautifulSoup(response.content, 'lxml')

# Identify table to scrape by inspecting site
table_node = soup.find(class_='flip-main')

# Find all 'span' elements in the table
columns_html = table_node.find_all('span')

# Extract the text
columns = [col.text for col in columns_html]

# This line extracts all 'span' tags inside 'p' tags within the table_node
spans_in_p = table_node.find('p').find_all('span')




"""



################################## Graveyard #################################







# We will now iterate through all the properties and scrape the necessary data 

#Vi starter i <div, infinite-scroller infinite-scroller-callback = "vm.infiniteScrollerCallback", class = "result-gallery-wrapper"
# Under den har hvert hus sin egen <section. Dernæst skal man ind under den første <div, class = "tile".
# Dernæst skal man ind under den første <div, class = "flip-main"
#Dernæst skal man ind under den anden <div, class = "home-tile-info col-md-4 alpha"
#Til sidst skal man ind i <a, hvor ng-if = "!result.solgtBolig". Åben da det tilsvarende link i en ny fane, som er givet i ng-href = "link"