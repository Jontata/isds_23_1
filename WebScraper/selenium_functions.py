from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException,
                                        TimeoutException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from time import sleep
import os
import re

def custom_find_my_element(driver, xpath, DELAY):
    retries = 3
    while retries > 0:
        try:
            # Wait for the presence of the element
            element = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.XPATH, xpath)))
            # Wait for the element to be visible
            WebDriverWait(driver, DELAY).until(EC.visibility_of(element))
            # Wait for the element to be clickable
            clickable_element = WebDriverWait(driver, DELAY).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return clickable_element
        except TimeoutException:
            print("<t>")
            sleep(1)
            retries -= 1
        except StaleElementReferenceException:
            print("<s>")
            sleep(1)
            retries -= 1
        except NoSuchElementException:
            print("<n>")
            sleep(1)
            retries -= 1
        except Exception as e:
            print(f"Other error {e}")
            sleep(1)
    print(f"Error w/ {xpath}")
    raise Exception

def wait_for_new_page_element(driver, xpath):
    try:
        custom_find_my_element(driver, xpath)
        return True
    except TimeoutException:
        return False

class myBusyException(Exception):
    pass

def click_and_wait_for_new_page(driver, element_xpath, new_page_element_xpath):
    max_retries=3
    retries = 0
    new_page_loaded = False
    while retries < max_retries and not new_page_loaded:
        try:
            clickable_element = custom_find_my_element(driver, element_xpath)
            clickable_element.click()
            new_page_loaded = wait_for_new_page_element(driver, new_page_element_xpath)
            if not new_page_loaded:
                print("New page not loaded. Retrying...")
                retries += 1
        except Exception as e:
            if retries > 1:
                print(str(e))
            if len(driver.find_elements(By.XPATH, "//div[@id='msgContainer']//*[contains(text(), 'currently being processed by')]")) > 0:
                raise myBusyException("Client Busy")
            print("Click retrying:")
            sleep(2)
            retries += 1
    if new_page_loaded:
        return new_page_loaded
    else:
        print(f"Failed to find new page element for {element_xpath}")
        raise Exception