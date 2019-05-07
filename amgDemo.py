from BandcampSpider import ProfileSpider


amgProfile = "https://bandcamp.com/angrymetalguy"

amgSpider = ProfileSpider(amgProfile,logfile="./demoResources/out/amgLog.txt")


amgSpider.getCollection()
amgSpider.to_csv("./demoResources/amg.csv")