from BandcampSpider import AlbumSpider
import pandas as pd

# Run if not already loaded
# import demoFrontPage


def getSupporterCount(url):
    try:
        tempAlbum = AlbumSpider(url, logfile="./demoResources/out/albumLog.txt")
        outval = len(tempAlbum.getSupporters(pageLimit=20))
        del tempAlbum
    except:
        outval = 0
    return outval


URLframe = pd.read_csv("./demoResources/demoFrontPage.csv")
URLframe = URLframe.groupby("genre").filter(lambda x: len(x) > 150).groupby("genre").head(25)

URLframe["supporter count"] = URLframe.url.apply(getSupporterCount)
URLframe.drop(["category"],axis=1,inplace=True)

URLframe.to_csv("./demoResources/supporterCounts.csv")