# This spider harvests URLs from the suggestions box about halfway down the page

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import pandas as pd
import numpy as np


from .SpiderClass import Spider
from .Exceptions import DomainError, PageTypeException



class FrontPageSpider(Spider):
    def __init__(self,genres, categories, driver_="Chrome",verbose=False):
        Spider.__init__(self, url="https://bandcamp.com", driver_=driver_,verbose=verbose, logfile="./frontPageLog.txt")

        self._genres = genres
        self._categories = categories
        self._Dict = None
        

    @staticmethod
    def getCategoryOptions():
        """ Static method to list options for categories to search
            Only 'top' and 'new' are currently functional """
        # if categories is recommended append "&r=most" to URL
        return ["top", "new", "rec"]

    @staticmethod
    def getGenreOptions():
        """ Static method to list genre options available to scrape
            on front page """
        return ["electronic", "rock", "metal", "alternative", "hip-hop-rap", "experimental", "punk", "folk", "pop", "ambient", "soundtrack",
                "world", "jazz", "acoustic", "funk", "r-b-soul", "devotional", "classical", "reggae", "podcasts", "country", "spoken-word",
                "comedy", "blues", "kids", "audiobooks", "latin"]
        
    def printURLs(self):
        for genre,cat_dict in self._Dict.items():
            for cat, url_list in cat_dict.items():
                for i,j in enumerate(url_list):
                    print(f'({genre},{cat}) {i}:  {j}')

    def getURLs(self, pageWaitTime=3, pageSleepTime=0.5, pageLimit=999, reset=False):
        if self._Dict == None or reset:
            self._populateDict(pageWaitTime=pageWaitTime,pageSleepTime = pageSleepTime, pageLimit=pageLimit)
        return self._Dict.copy()


    def _populateDict(self, pageWaitTime = 3, pageSleepTime=0.5,pageLimit=25, startPage=0):
        self._Dict={}
        for genre in self._genres:
            genre_acc = {}
            for category in self._categories:
                # note p=page, g=genre, s=category in string formatting
                # best selling items previewed are shown in 200 pages for each category
                self._driver.get(f'https://bandcamp.com/?g={genre}&s={category}&p={startPage}&gn=0&f=all&w=0')

                # Scroll to half the page to hit top suggestions
                # Wait for load
                # Dummy is created to force load of elements grabbed in links
                self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                try:
                    waiter = WebDriverWait(self._driver, pageWaitTime)
                    dummy = waiter.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="item-title"]')))
                except Exception as e:
                    self._loadHandler(f'({genre},{category})',e)
                    continue

                
                # Click through to load all suggestions
                counter = 0
                while(True and counter < pageLimit):
                    try:
                        buttonTimer = WebDriverWait(self._driver,pageWaitTime)
                        button = buttonTimer.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="item-page"][./text() = "next"]')))
                        button.click()
                        time.sleep(pageSleepTime)
                        counter += 1
                    except:
                        break
                try:
                    links = self._driver.find_elements_by_xpath('//a[@class="item-title"]')
                except Exception as e:
                    self._exceptHandler(f'links for ({genre},{category}) on page {counter}',e,verbose=True)
                    links = []
                finally:
                    genre_acc[category] = [re.sub("\?from.*$", "", i.get_attribute('href')) for i in links]
            self._Dict[genre] = genre_acc

    def asDataFrame(self):
        def arrayGen(d):
            for genre, cat_dict in d.items():
                for category, url_list in cat_dict.items():
                    for i in url_list:
                        yield [genre,category,i]
        
        return pd.DataFrame(np.array(list(arrayGen(self._Dict))), 
                columns = ["genre","category","url"])


    def to_csv(self, fileName):
        """ Outputs URLs gathered to CSV """
        self.asDataFrame().to_csv(fileName,index=False)


