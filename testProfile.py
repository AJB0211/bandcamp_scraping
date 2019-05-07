import BandcampSpider

test_URL = "https://bandcamp.com/AJB0211"
# test_URL = "https://bandcamp.com/stevenvlass"

test = BandcampSpider.ProfileSpider(test_URL)


# print(test._collectionSize)
# print(test._wishlistSize)
# print(test._numFollowers)
# print(test._numFollowing)
collection = test.getCollection(stopTime=4)
# selfDict = test.getAsDict()


# for i in collection:
#     print(i)

# print("\n")


# for i,j in selfDict.items():
#     print(f'{i}:{j}')


# for i in test.getWishlist():
#     print(i)

print(test.asPandasSeries())

test.to_csv("./demoResources/myProfile.csv")

del test