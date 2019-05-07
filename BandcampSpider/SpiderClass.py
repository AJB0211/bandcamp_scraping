from selenium import webdriver
import re

from .Exceptions import DomainError,PageTypeException

class Spider(object):
    def __init__(self,url,driver_="Chrome",verbose=False,logfile="./log.txt"):
        if re.search("bandcamp",url) == None:
            raise DomainError("Not in the Bandcamp domain")
        if driver_ == "Chrome":
            self._driver = webdriver.Chrome("./chromedriver")
        self._url = url
        self._driver.get(self._url)
        self._logFile = open(logfile,"w+")

    def _exceptHandler(self, field, e: Exception, verbose=False):
        exceptStr = f'{self._url}:\n Failed to grab {field} with {e}\n\n'
        self._logFile.write(exceptStr)
        if verbose:
            print(exceptStr)

    def _loadHandler(self, field, e: Exception, verbose=False):
        exceptStr = f'{field} did not load quickly enough. Produced an {e}.'
        self._logFile.write(exceptStr)
        if verbose:
            print(exceptStr)

    def __del__(self):
        self._logFile.close()
        self._driver.quit()
