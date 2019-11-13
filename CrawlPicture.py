from bs4 import BeautifulSoup
import requests, json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import pandas as pd


def getMoviePoster(moviename):
    url = "http://global.bing.com/images/search?q=" + moviename + " poster&qft=+filterui:imagesize-large&FORM=R5IR5"
    soup = BeautifulSoup(requests.get(url).text, features="html5lib")
    images = [a["src"] for a in soup.find_all("img", {"alt": " "})]
    poster = images[0]
    poster = poster.replace("&", "&amp")
    return poster


def getDictionary():
    # don't forget to change html5lib to other libraries

    API_movie_URL = "https://casecomp.konnectrv.io/movie"
    r = requests.get(url=API_movie_URL)
    r = r.json()
    movieDictionary = {}
    count = 0

    for i in r:
        url = "https://www.imdb.com/title/" + i['imdb']
        soup = BeautifulSoup(requests.get(url).text, features='html5lib')

        url = "https://www.imdb.com/title/" + i['imdb'] + "/ratings"
        soup_rating = BeautifulSoup(requests.get(url).text, features='html5lib')

        imdbdata = soup.find_all("script", type='application/ld+json')
        ratedata = [float(a.get_text().strip().strip("%")) * 0.01 for a in
                    soup_rating.find_all("div", {"class": "topAligned"})]
        # never do divisions

        dic = json.loads(imdbdata[0].get_text())

        movieDictionary[i['title']] = {}
        movieDictionary[i['title']]["release_date"] = i['release_date']
        movieDictionary[i['title']]['rating'] = i['rating']
        movieDictionary[i['title']]['streaming_platform'] = i['streaming_platform']
        movieDictionary[i['title']]['production_companies'] = i['production_companies']
        movieDictionary[i['title']]['overview'] = i['overview']

        # imdb data
        movieDictionary[i['title']]['genre'] = dic['genre']
        movieDictionary[i['title']]['posterURL'] = getMoviePoster(i['title'])
        movieDictionary[i['title']]['imdb'] = i['imdb']
        movieDictionary[i['title']]['imdb_score'] = dic['aggregateRating']['ratingValue']
        movieDictionary[i['title']]['ratedata'] = ratedata  # percentage from voting point 10 to point 1
        movieDictionary[i['title']]['cast'] = [a['name'] for a in dic['actor']]
        castURL = ["https://www.imdb.com" + a['url'] for a in dic['actor']]
        castImage = []
        for cast in castURL:
            soupCast = BeautifulSoup(requests.get(cast).text, features='html5lib')
            urldata = soupCast.find_all("script", type='application/ld+json')
            castDic = json.loads(urldata[0].get_text())
            if 'image' in castDic:
                castImage.append(castDic['image'])
            else:
                castImage.append(None)

        movieDictionary[i['title']]['castImage'] = castImage

        if 'image' in dic.keys():
            movieDictionary[i['title']]['posterURL'] = dic['image']
        else:
            movieDictionary[i['title']]['posterURL'] = getMoviePoster(i['title'])
        print(count)
        count += 1
    return movieDictionary


def getCommentCloudMap(movieName):
    global stopwords
    imdbID = "tt4633694"

    # get the movie poster here, modify here
    colorArray = cv.imread("th.jpg")
    posterColor = ImageColorGenerator(colorArray)

    imgray = cv.cvtColor(colorArray, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    maskArray, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    url = "https://www.imdb.com/title/" + imdbID + "/reviews?ref_=tt_urv"
    soup = BeautifulSoup(requests.get(url).text, features='html5lib')
    comments = soup.find_all("div", class_='text show-more__control')
    length = max(25, len(comments))
    comments = comments[:length]
    commentsWithoutTag = [comment.get_text() for comment in comments]
    commentsStr = " ".join(commentsWithoutTag)

    wc = WordCloud(stopwords=stopwords, background_color="white", mask=maskArray, contour_width=3,
                   contour_color='firebrick').generate(commentsStr)

    plt.imshow(wc.recolor(color_func=posterColor), interpolation='bilinear')
    plt.axis("off")
    plt.show()


# using pandas here to calculate percentage
def getPercentageBetter(dictionary):
    global comparisonFrame
    dictFrame = pd.DataFrame.from_dict(dictionary)
    dictFrame = dictFrame.transpose()
    comparisonFrame = dictFrame
    dictFrame = dictFrame.apply(getComparisonPercentage, axis=1)
    # return dictFrame[['genreBetterPercentage', 'allBetterPercentage']]
    print(dictFrame[['genreBetterPercentage', 'allBetterPercentage']])


def getComparisonPercentage(row):
    global comparisonFrame
    allBetterFrame = comparisonFrame[comparisonFrame['imdb_score'] < row['imdb_score']]
    allBetterPercentage = allBetterFrame['imdb_score'].count() / comparisonFrame.count().iloc[0]
    genreCount = 0
    genreBetterCount = 0
    # Only use the first genre of the list, maybe you want to elimnate 0 value in the GenreBetterPercentage
    genre = row['genre'][0]
    for i in comparisonFrame.index:
        if genre in comparisonFrame.loc[i]['genre']:
            genreCount += 1
            if i in allBetterFrame.index:
                genreBetterCount += 1
    genreBetterPercentage = genreBetterCount / genreCount
    row[
        "genreBetterPercentage"] = genreBetterPercentage  # better than how much percentage of the films of the same genre (first genre in the list)
    row['allBetterPercentage'] = allBetterPercentage  # better than how much percentage of all films
    return row


# dictionary = getDictionary()

# store the dictionary into local, no need to do so
# with open('dic.txt', 'w') as file:
#     file.write(json.dumps(dictionary))

dictionaryTxt = json.loads(open('dic.txt', 'r').read())
comparisonFrame = 0
result = getPercentageBetter(dictionaryTxt)
# print(result)


# stopwords = set(STOPWORDS)
# stopwords.update(["movie", "film", "series", "show", "done", "watch", "see", "us", "story", "scene", "many"])
# getCommentCloudMap("a")
# for r in dictionary:
#     print(r)
#     print(dictionary[r])
#     print()