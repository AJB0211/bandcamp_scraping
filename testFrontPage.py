

from BandcampSpider import FrontPageSpider

# change to 200 for use
test_cat = ["top"]
test_gen = ["electronic"]#, "rock", "metal"]


test = FrontPageSpider(genres = test_gen,categories = test_cat )

test.getURLs(pageLimit=5,pageSleepTime=2,pageWaitTime=5)
test.printURLs()
print(test.asDataFrame().genre.value_counts())

#test.to_csv("./demoResources/demoFrontPage.csv")

del test
