# Bandcamp Scraping Project

## Purpose
Scrape the front page of bandcamp to obtain links to current albums. Then from those albums grab relevant information as well as users that supported that album.


### v1.1.1
  * Removed redundant or unnecessary files files from repo
  * Updates to demo.ipynb
  * Minor changes to logfile handling in constructors
  * Bug fix in exception handler
  * Introduced readSeries static method accessible from all classes to handle reading csv outputs to pandas.Series


### v1.1.0
  * Restructured to properly load as library
  * Added conversions to pandas objects and CSV files
  * Added wait timer and page number arguements to scraping operations
  * Test files
  * Demo

### v1.0.0
  * Introduced exceptions
  * Introduced Profile spider, completed collection URL scraping
    + BUG: Cannot expand wishlist currently. Issue with "view all..." button
  * Refactored front page spider into class structure
  * Version updated to reflect usable state of library

### v0.2.2
  * Restructured repo for legibility and library implementation

### v0.2.1
 * Added base spider class for driver and exception handling
 * Finalized iteration of AlbumSpider class inheriting from Spider

### v0.1.2
 * Changed project file name for generalization
 * Added general scraping of front page suggestions URLs to dictionary
   + Future work: generalize to class structure
 * Created album spider class
   + Grabs album, band, label, and digital album prices

### v0.1.1
 * Repo initialization
 * Selenium barebones
