from selenium import webdriver



class Spider(object):
    def __init__(self,url,driver_="Chrome",verbose=False,logfile="./log.txt"):
        if driver_ == "Chrome":
            self._driver = webdriver.Chrome("./chromedriver")
        self.__url = url
        self._driver.get(self.__url)
        self.__logFile = open(logfile,"w+")

    def __exceptHandler(self, field, e: Exception, verbose=False):
        exceptStr = f'{self.__url}:\n Failed to grab {field} with {e}\n\n'
        self._Spider__logFile.write(exceptStr)
        if verbose:
            print(exceptStr)

    def __del__(self):
        self._Spider__logFile.close()
        self._driver.quit()