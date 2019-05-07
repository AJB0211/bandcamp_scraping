from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import timedelta
import re
import numpy as np
import pandas as pd

from .SpiderClass import Spider
from .Exceptions import DomainError, PageTypeException



class ProfileSpider(Spider):
    def __init__(self, url, driver="Chrome", verbose=False, logfile="./ProfileLog.txt"):
        Spider.__init__(self, url=url, driver_=driver, verbose=verbose, logfile=logfile)
        self._username = self._driver.find_element_by_xpath('//span[@data-bind="text: name"]').text
        self._collection = None                          # List of URLs of owned albums
        self._wishlist = None                            # List of URLs of albums on wishlist
        try:
            self._collectionSize = int(self._driver.find_element_by_xpath('//li[@data-tab="collection"]//span[@class="count"]').text)
        except:
            self._collectionSize = 0
        try:
            self._wishlistSize = int(self._driver.find_element_by_xpath('//li[@data-tab="wishlist"]//span[@class="count"]').text)
        except:
            self._wishlistSize = 0
        try:
            self._numFollowers = int(self._driver.find_element_by_xpath('//li[@data-tab="followers"]//span[@class="count"]').text)
        except:
            self._numFollowers = 0
        try:
            self._numFollowing = int(self._driver.find_element_by_xpath('//li[@data-tab="following"]//span[@class="count"]').text)
        except:
            self._numFollowing = 0

    def getUsername(self):
        return self._username

    def getAsDict(self):
        if self._collection == None:
            out_collection = ""
        else:
            out_collection = ",".join(self._collection)
        if self._wishlist == None:
            out_wishlist = ""
        else:
            out_wishlist = ",".join(self._wishlist)
        return {"username": self._username,
                 "collectionSize": self._collectionSize,
                 "wishlistSize": self._wishlistSize,
                 "followers": self._numFollowers,
                 "following": self._numFollowing,
                 "collection": out_collection,
                 "wishlist": out_wishlist
                 }

    def _scrollMe(self,target,scroller,stopTime=2,pageNum="All"):
        """ Used to scroll down to load dynamic page elements """
        floor = self._driver.find_element_by_xpath('//div[@id="pgFt"]')
        self._driver.execute_script("arguments[0].scrollIntoView(true);", floor)
        old_count = len(self._driver.find_elements_by_xpath(target))
        try:
            buttonTimer = WebDriverWait(self._driver,2)
            button = buttonTimer.until(EC.element_to_be_clickable((By.XPATH,scroller)))
            button.click()
        except NoSuchElementException:
            return
        except Exception as e:
            self._exceptHandler("Scroll button",e,verbose=False)
        
        if pageNum=="All":
            maxPages = 999
        else:
            maxPages = pageNum
        
        counter = 0
        while(counter < maxPages):
            floor = self._driver.find_element_by_xpath('//div[@id="pgFt"]')
            heightWait = WebDriverWait(self._driver,15)
            try:
                heightWait.until(EC.visibility_of_all_elements_located((By.XPATH,target)))
            except Exception as e:
                print(e)
                break
            time.sleep(stopTime/2.0)
            self._driver.execute_script("arguments[0].scrollIntoView(true);",floor)
            time.sleep(stopTime/2.0)
            new_count = len(self._driver.find_elements_by_xpath(target))
            if new_count == old_count:
                break
            else:
                old_count = new_count
                counter += 1




    def _populateCollection(self,stopTime=2,pageNum=999,verbose=False):
        """ Internal setter for getting items in a user's collection as a list of URLs"""
        if self._collectionSize == 0:
            self._collection = []
        self._driver.get(self._url)
        if self._collectionSize > 40:
            target = '//li[@class="collection-item-container track_play_hilite"]'
            self._scrollMe(target=target,scroller='//button[@class="show-more"]', pageNum=pageNum,stopTime=stopTime)
        else:
            target = '//li[@class = "collection-item-container track_play_hilite   "]'
        items = self._driver.find_elements_by_xpath(target+'//div[@class="collection-title-details"]//a[@class="item-link"]')
        self._collection = [i.get_attribute('href') for i in items]


    def getCollection(self, stopTime=2, pageNum=999, reset = False):
        """ External getter for collection as a list of URLs """
        if self._collection == None or reset:
            self._populateCollection(stopTime = stopTime,pageNum=pageNum)
        return self._collection.copy()


    ### Currently the button for the wishlist is not clickable. Unsure of why. Fix in future update
    def _populateWishlist(self,pageNum=999,verbose=False):
        """ Internal setter for getting items in a user's wishlist as a list of URLs"""
        if self._wishlistSize == 0:
            self._wishlist = []
        self._driver.get(self._url+"/wishlist")
        if self._wishlistSize > 40:
            target = '//li[@class="collection-item-container track_play_hilite"]'
            self._scrollMe(
                target=target, scroller='//div[@class="expand-container show-button"]/button', pageNum=pageNum)
        else:
            target = '//li[@class = "collection-item-container track_play_hilite   "]'
        items = self._driver.find_elements_by_xpath(target+'//div[@class="collection-title-details"]//a[@class="item-link"]')
        self._wishlist = [i.get_attribute('href') for i in items]

    
    def getWishlist(self, reset = False):
        """ External getter for wishlist as a list of URLs """
        if self._wishlist == None or reset:
            self._populateWishlist(pageNum=5)
        return self._wishlist.copy()


    def asPandasSeries(self):
        """ Converts profile object into pandas Series """
        return pd.Series(self.getAsDict())

    def to_csv(self,filename):
        """ Converts profile object into csv file """
        self.asPandasSeries().to_csv(filename, header=False)
