from selenium import webdriver
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


# release date

## Future work: grab other distribution formats
## Mostly concerned with digital but vinyl is interesting too



from SpiderClass import Spider

class AlbumSpider(Spider):
    def __init__(self,url, driver="Chrome", verbose=False):
        Spider.__init__(self,url=url,driver_=driver,verbose=verbose,logfile="./albumLog.txt")
        self.__scrollBool = False
        self._AlbumSpider__PopulateAlbumDetails(verbose=verbose)
        self.__reviews = None       # Dictionary of review details
        self.__supporters = None    # List of supporter URLS

    # Gets object details from web again
    def resetAlbumDetails(self, verbose=False):
        self._AlbumSpider_PopulateAlbumDetails(verbose=verbose)

    # Internal setter from web for album genre tags
    def __populateTags(self):
        try:
            tags = self._driver.find_elements_by_xpath('//div[@class="tralbumData tralbum-tags tralbum-tags-nu"]//a[@class="tag"]')
            self._tags = [i.text for i in tags]
        except Exception as e:
            self._Spider__exceptHandler("tags",e)
            self._tags = []

    # Internal setter for price from web
    # Only finds digital prices
    def __populatePrice(self):
        try:
            self._price = self._driver.find_element_by_xpath(
                '//h4[@class="ft compound-button main-button"]//span[@class="base-text-color"]').text
        except:
            try:
                self._price = self._driver.find_element_by_xpath(
                    '//h4[@class="ft compound-button main-button"]//span[@class="buyItemExtra buyItemNyp secondaryText"]').text
            except:
                self._price= "No Digital Sale"

    def __SongDetails(self,verbose = False):

        def songHandler(song):
            songNumber = int(song.find_element_by_xpath('.//div[@class="track_number secondaryText"]').text.replace(".",""))
            songName = song.find_element_by_xpath('.//span[@itemprop="name"]').text
            songTime = song.find_element_by_xpath('.//span[@class="time secondaryText"]').text
            try:
                t = time.strptime(songTime,"%M:%S")
            except ValueError:
                t = time.strptime(songTime,"%H:%M:%S")
            except Exception as e:
                self._Spider__exceptHandler("songDuration",e)
                t = time.strptime("0:0","%M:%S")
            songDuration = timedelta(hours=t.tm_hour,minutes=t.tm_min,seconds=t.tm_sec).total_seconds()

            return {"track": songNumber,"title":songName,"duration":songDuration}

        try:
            songs = self._driver.find_elements_by_xpath('//tr[@class="track_row_view linked"]')
            self._songList = [songHandler(i) for i in songs]
            
        except Exception as e:
            self._Spider__exceptHandler("songs",e,verbose)
            self._songList = []
        
        self._albumDuration = 0
        for song in self._songList:
            self._albumDuration += song["duration"]


    # Internal set for getting album details from web
    def __PopulateAlbumDetails(self, verbose=False):
        try:
            self._albumTitle = self._driver.find_element_by_xpath('//h2[@class="trackTitle"]').text
        except Exception as e:
            self._Spider__exceptHandler("albumTitle",e)
            self._albumTitle = ""
        try:    
            self._bandName = self._driver.find_element_by_xpath('//span[@itemprop="byArtist"]/a').text
        except Exception as e:
            self._Spider__exceptHandler("bandName", e)
            self._bandName = ""
        try:
            self._label = self._driver.find_element_by_xpath('//p[@id="band-name-location"]/span[@class="title"]').text
        except Exception as e:
            self._Spider__exceptHandler("label", e)
            self._label = ""

        try: 
            self._releaseDate = self._driver.find_element_by_xpath('//meta[@itemprop="datePublished"]').get_attribute('content')
        except Exception as e:
            self._Spider__exceptHandler("release date",e,verbose=True)
            self._releaseDate = ""
        
        self._AlbumSpider__populatePrice()
        self._AlbumSpider__populateTags()
        self._AlbumSpider__SongDetails()
        


    # Getter for external album details dictionary
    def getAlbumDetails(self):
        return {"albumTitle": self._albumTitle,
                "bandName": self._bandName,
                "label": self._label,
                "price": self._price,
                "tags": self._tags,
                "songs": self._songList,
                "totalDuration": self._albumDuration,
                "releaseDate": self._releaseDate}

    # Internal get supporters from web
    def __populateSupporters(self):
        if not self._AlbumSpider__scrollBool:
            self._driver.execute_script("window.scroll(0,300)")
            self._AlbumSpider__scrollBool = True
        try:
            button = self._driver.find_element_by_xpath('//a[@class="more-writing"][./text()="more..."]')
            button.click()
        except NoSuchElementException:
            pass
        except Exception as e:
            self._Spider__exceptHandler("reviewers",e)
        
        while(True):
            try:
                moreTimer = WebDriverWait(self._driver,3)
                button = moreTimer.until(EC.element_to_be_clickable((By.XPATH,'//a[@class="more-thumbs"][./text()= "more..."]')))
                button.click()
                time.sleep(0.1)
                #self._driver.execute_script("window.scroll(0,200)")
            except NoSuchElementException:
                break
            except Exception as e:
                self._Spider__exceptHandler("more supporters",e,verbose=True)
        try:
            reviewers = self._driver.find_elements_by_xpath('//a[@class="pic"]')
            supporters = self._driver.find_elements_by_xpath('//a[@class="fan pic"]')
            return [re.sub("\?from.*$","",i.get_attribute('href')) for i in reviewers+supporters]
        except Exception as e:
            self._Spider__exceptHandler("supporters",e,verbose=True)

    # External getter for supporters URL list
    def getSupporters(self,count=None, reset=False):
        if self._AlbumSpider__supporters == None or reset==True:
            self._AlbumSpider__supporters = self._AlbumSpider__populateSupporters()
        return self._AlbumSpider__supporters.copy()


    # External getter for reviews dictionary
    def getReviews(self,reset=False):
        if self._AlbumSpider__reviews == None or reset==True:
            self._AlbumSpider__reviews = self._AlbumSpider__populateReviews()
        return self._AlbumSpider__reviews.copy()

    # Internal setter for reviews dictionary from web
    def __populateReviews(self):
        if not self._AlbumSpider__scrollBool:
            self._driver.execute_script("window.scroll(0,300)")
            self._AlbumSpider__scrollBool = True
        try:
            moreTimer = WebDriverWait(self._driver, 3)
            button = moreTimer.until(EC.visibility_of_element_located((By.XPATH,'//a[@class="more-writing"][./text()="more..."]')))
            button.click()
            waiter = WebDriverWait(self._driver, 3)
            dummy = waiter.until(EC.visibility_of_element_located((By.XPATH, '//a[@class="more-writing"][@style="display: none;"]')))
        except NoSuchElementException:
            pass
        except Exception as e:
            self._Spider__exceptHandler("reviewers", e)

        reviews = self._driver.find_elements_by_xpath('//div[@class="writing"]')

        # Helper function for following list comprehension
        def reviewCleaner(review):
            revDict = {}
            revDict["url"] = review.find_element_by_xpath('.//a[@class="name notSkinnable"]').get_attribute('href')
            revDict["reviewer"] = review.find_element_by_xpath('.//a[@class="name notSkinnable"]').text
            try:
                revDict["favoriteTrack"] = re.sub("Favorite\strack:\s", "", review.find_element_by_xpath('.//span[@class="fav-track"]').text)
            except:
                revDict["favoriteTrack"] = "::NULL::"
            revDict["review"] = re.sub(f'({revDict["reviewer"]}\s)|(Favorite\strack:.*)',"",review.find_element_by_xpath('.//div[@class="text"]').text)
            revDict["album"] = self._albumTitle
            revDict["band"] = self._bandName
            return revDict
        
        return [reviewCleaner(i) for i in reviews]



#### Below is for testing


## Example of sale but not digital sale
# testURL = "https://septicflesh.bandcamp.com/album/titan"
## Example of only merch
# testURL = "https://septicflesh.bandcamp.com/album/codex-omega"

# testURL = "https://deathspellomega.bandcamp.com/album/the-furnaces-of-palingenesia"

# testURL = "https://archivistmusic.bandcamp.com/album/construct"
# testURL = "https://comebackkid-hc.bandcamp.com/"
testURL = "https://aenimus.bandcamp.com/"

## Example of song over an hour
testURL = "https://bellwitch.bandcamp.com/album/mirror-reaper"

test = AlbumSpider(testURL)

testDict = test.getAlbumDetails()
for i,j in testDict.items():
    print(f'{i} : {j}')

# for d in test.getReviews():
#     for i,j in d.items():
#         print(f'{i}:{j}')
#     print('\n\n')


# for i in test.getSupporters():
#     print(i)


del test
