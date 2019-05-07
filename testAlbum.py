

import BandcampSpider


#### Below is for testing


## Example of sale but not digital sale
# testURL = "https://septicflesh.bandcamp.com/album/titan"
## Example of only merch
# testURL = "https://septicflesh.bandcamp.com/album/codex-omega"

# testURL = "https://deathspellomega.bandcamp.com/album/the-furnaces-of-palingenesia"

# testURL = "https://archivistmusic.bandcamp.com/album/construct"
# testURL = "https://comebackkid-hc.bandcamp.com/"
testURL = "https://aenimus.bandcamp.com/"

## Example of song over an hour
# testURL = "https://bellwitch.bandcamp.com/album/mirror-reaper"

# testURL = "https://bandcamp.com"

test = BandcampSpider.AlbumSpider(testURL)

testDict = test.getAlbumDetails()
for i, j in testDict.items():
    print(f'{i} : {j}')

# for d in test.getReviews():
#     for i,j in d.items():
#         print(f'{i}:{j}')
#     print('\n\n')


# for i in test.getSupporters():
#     print(i)


del test
