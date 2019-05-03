from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time


# release date, supporters


driver=webdriver.Chrome("./chromedriver")


## Future work: grab other formats
## Mostly concerned with digital but vinyl is interesting too

## Example of sale but not digital sale
# testURL = "https://septicflesh.bandcamp.com/album/titan"
## Example of only merch
# testURL = "https://septicflesh.bandcamp.com/album/codex-omega"

# testURL = "https://deathspellomega.bandcamp.com/album/the-furnaces-of-palingenesia"

class albumSpider(object):
    def __init__(self,url):
        self._driver = webdriver.Chrome("./chromedriver")
        self._driver.get(url)
        self.getAlbumDetails()


    def getAlbumDetails(self):
        self._albumTitle = self._driver.find_element_by_xpath('//h2[@class="trackTitle"]').text
        self._bandName = self._driver.find_element_by_xpath('//span[@itemprop="byArtist"]/a').text
        self._label = self._driver.find_element_by_xpath('//p[@id="band-name-location"]/span[@class="title"]').text
        try:
            self._price = self.driver.find_element_by_xpath(
                '//h4[@class="ft compound-button main-button"]//span[@class="base-text-color"]').text
                #'//li[@class=buyItem digital//h4[@class="ft compound-button main-button"]//span[@class="base-text-color"]').text
        except Exception as e:
            #print(e)
            try:
                self._price = driver.find_element_by_xpath(
                    '//h4[@class="ft compound-button main-button"]//span[@class="buyItemExtra buyItemNyp secondaryText"]').text
            except:
                self._price="No Digital Sale"
                #print("not price grabbing method works")f


    def getAsDict(self):
        return {"albumTitle": self._albumTitle,
                "bandName": self._bandName,
                "label": self._label,
                "price": self._price}


testURL = "https://archivistmusic.bandcamp.com/album/construct"
test = albumSpider(testURL)
for i,j in test.getAsDict().items():
    print(f'{i} : {j}')
