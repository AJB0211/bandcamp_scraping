from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome("./chromedriver")
genres = ["electronic","rock","metal","alternative","hip-hop-rap","experimental","punk","folk","pop","ambient","soundtrack",
            "world", "jazz", "acoustic","funk","r-b-soul","devotional","classical","reggae","podcasts","country","spoken-word",
            "comedy","blues","kids","audiobooks","latin"]
categories = ["top","new","rec"]

#if categories is recommended append "&r=most" to URL


albumList = []
# change to 200 for use
test_cat = ["top"]
test_gen = ["metal"]

for gen in test_gen:
    for cat in test_cat:
        acc = []
        # note p=page, g=genre, s=category in string formatting
        # best selling items previewed are shown in 200 pages for each category
        driver.get(f'https://bandcamp.com/?g={gen}&s={cat}&p=0&gn=0&f=all&w=0')

        # Scroll to half the page to hit top suggestions
        # Wait for load
        # Dummy is created to force load of elements grabbed in links
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        waiter = WebDriverWait(driver, 1)
        dummy = waiter.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="item-title"]')))


        # These are the actual links off each page I want
        links = driver.find_elements_by_xpath('//a[@class="item-title"]')
        acc.append(*[i.get_attribute('href') for i in links])


for i,j in enumerate(acc):
    print(f'{i}:   {j}\n')
#'//*[@id="discover"]/div[9]/div[1]/div[2]/div[1]/a[2]'
#get_attribute('href')
#for i in table:
 #   print(i.get_attribute('href'))
