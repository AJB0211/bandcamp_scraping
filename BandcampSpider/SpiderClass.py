from selenium import webdriver
import re
import pandas as pd

from .Exceptions import DomainError,PageTypeException

class Spider(object):
    def __init__(self,url,driver_="Chrome",verbose=False,logfile="./log.txt"):
        self._url = url
        self._logFile = open(logfile, "w+")
        if re.search("bandcamp",url) == None:
            raise DomainError("Not in the Bandcamp domain")
            self._logFile.write(f'DomainError at {self._url}\n')
            del self
        if driver_ == "Chrome":
            self._driver = webdriver.Chrome("./chromedriver")
        self._driver.get(self._url)


    
    @staticmethod
    def readSeries(filepath):
        tempDF = pd.read_csv(filepath,index_col=False,header=None,squeeze=True)
        return pd.Series(tempDF[1].values,index=tempDF[0])

    def _exceptHandler(self, field, e: Exception, verbose=False):
        exceptStr = f'{self._url}:\n Failed to grab {field} with {type(e)}\n\n'
        self._logFile.write(exceptStr)
        if verbose:
            print(exceptStr)

    def _loadHandler(self, field, e: Exception, page,verbose=False):
        exceptStr = f'{field} did not load quickly enough. Produced an {type(e)}.\nOn page {page}.'
        self._logFile.write(exceptStr)
        if verbose:
            print(exceptStr)

    def __del__(self):
        self._logFile.close()
        self._driver.quit()
