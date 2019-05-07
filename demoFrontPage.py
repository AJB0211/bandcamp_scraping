

from BandcampSpider import FrontPageSpider

# change to 200 for use
test_cat = ["top"]
test_gen = ["electronic", "rock", "metal", "alternative", "hip-hop-rap", "experimental", "punk", "folk", "pop", "ambient", "soundtrack",
            "world", "jazz", "acoustic", "funk", "r-b-soul", "devotional", "classical", "reggae", "country", "spoken-word",
            "comedy", "blues"]


test = FrontPageSpider(genres = test_gen,categories = test_cat )

test.getURLs(pageLimit=20,pageSleepTime=2,pageWaitTime=5)
#test.printURLs()
#print(test.asDataFrame().head())

test.to_csv("./demoResources/demoFrontPage.csv")

del test
