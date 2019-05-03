from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time


driver = webdriver.Chrome("./chromedriver")
genres = ["electronic","rock","metal","alternative","hip-hop-rap","experimental","punk","folk","pop","ambient","soundtrack",
            "world", "jazz", "acoustic","funk","r-b-soul","devotional","classical","reggae","podcasts","country","spoken-word",
            "comedy","blues","kids","audiobooks","latin"]
categories = ["top","new","rec"]

#if categories is recommended append "&r=most" to URL


albumList = []
# change to 200 for use
test_cat = ["top"]
test_gen = ["audiobooks"]


def find_element(elem):
    def find_driver(driver):
        element = driver.find_element_by_id(elem)
        if element:
            return element
        else:
            return False
    return find_driver


#element = WebDriverWait(driver, secs).until(find)

full_acc = {}
for genre in genres:
    genre_acc = {}
    for category in test_cat:
        # note p=page, g=genre, s=category in string formatting
        # best selling items previewed are shown in 200 pages for each category
        driver.get(f'https://bandcamp.com/?g={genre}&s={category}&p=0&gn=0&f=all&w=0')

        # Scroll to half the page to hit top suggestions
        # Wait for load
        # Dummy is created to force load of elements grabbed in links
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        try:
            waiter = WebDriverWait(driver, 3)
            dummy = waiter.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="item-title"]')))
        except:
            print(f'({genre},{category}) did not load quickly enough, skipped')
            continue

        
        # Click through to load all suggestions
        counter = 0
        # counter condition for testing
        while(True and counter < 10):
            try:
                find_button = find_element('//a[@class="item-page"][./text() = "next"]')
                buttonTimer = WebDriverWait(driver,1)#.until(find_button)
                button = buttonTimer.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="item-page"][./text() = "next"]')))
                button.click()
                time.sleep(0.25)
                counter += 1
            except:
                break
        
        # These are the actual links off each page I want
        try:
            links = driver.find_elements_by_xpath('//a[@class="item-title"]')
        except:
            print("*"*50)
            print(f'({genre},{category}) failed on page {counter}\n')
            print("*"*50)
            continue
        acc = [i.get_attribute('href') for i in links]
        genre_acc[category] = acc
    full_acc[genre] = genre_acc


def acc_gen(dict):
    for genre, cat_dict in full_acc:
        for cat, url_list in cat_dict:
            for i in enumerate(url_list):
                yield i

for i in acc_gen(full_acc):
    print(i)


# for genre, cat_dict in full_acc:
#     for cat, url_list in cat_dict:
#         for i in enumerate(url_list):
#             print(f'({genre},{cat}):    {i}')
#     print("*"*50)
