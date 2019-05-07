from BandcampSpider import AlbumSpider
import pandas as pd


#import .amgDemo


amgSeries = AlbumSpider.readSeries("./demoResources/amg.csv")

albums = amgSeries.collection.split(",")

def tagGet(i):
    try:
        tempSpider = AlbumSpider(i, logfile="./demoResources/out/amgAlbumLog.txt")
        out = tempSpider.getAlbumDetails()["tags"]
        del tempSpider
    except:
        out = []
    return out

#tagsList = [tagGet(i) for i in albums]
#tags = [j for sub in tagsList for j in sub]
tags = [j for i in albums for j in tagGet(i)]

pd.Series(tags).to_csv("./demoResources/amgTags.csv")