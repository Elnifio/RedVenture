from bs4 import BeautifulSoup
import requests, json
import django, os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import cv2 as cv
import pandas as pd
import urllib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redventure.settings')
django.setup()
stopwords = set(STOPWORDS)
stopwords.update(["movie", "film", "series", "show", "done", "watch", "see", "us", "story", "scene", "many"])

from crawler.models import Movie, Genre, Platform

def getMoviePoster(moviename = "Da Vinci Code"):
    url = "http://global.bing.com/images/search?q=" + moviename + " poster&qft=+filterui:imagesize-large&FORM=R5IR5"
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    images = [a["src"] for a in soup.find_all("img", {"alt": " "})]
    poster = images[0]
    poster = poster.replace("&", "&amp")
    return poster

def getDictionaryComparison():
    API_movie_URL = "https://casecomp.konnectrv.io/movie"
    r = requests.get(url = API_movie_URL)
    r = r.json()
    movieDictionary = {}
    for i in r:
        movieDictionary[i['title']] = {}
        movieDictionary[i['title']]["release_date"] = i['release_date']
        movieDictionary[i['title']]['rating'] = i['rating']
        movieDictionary[i['title']]['streaming_platform'] = i['streaming_platform']
        movieDictionary[i['title']]['production_companies'] = i['production_companies']
        movieDictionary[i['title']]['overview'] = i['overview']
        movieDictionary[i['title']]['posterURL'] = getMoviePoster(i['title'])
        movieDictionary[i['title']]['imdb'] = i['imdb']
    return movieDictionary

def updateAllPictures():
    API_movie_URL = "https://casecomp.konnectrv.io/movie"
    r = requests.get(url = API_movie_URL)
    r = r.json()
    for item in r:
        url = "https://www.imdb.com/title/" + item['imdb']
        soup = BeautifulSoup(requests.get(url).text, features='lxml')
        genre = [a for a in soup.find_all("script", type='application/ld+json')]
        dic = json.loads(genre[0].get_text())
        movie = Movie.objects.get(imdb=item['imdb'])
        movie.genre = json.dumps(dic['genre'])
        if 'image' in dic.keys():
            movie.image_link = dic['image']
        else:
            movie.image_link = getMoviePoster(item['title'])
        movie.save()


def createMovies():
    API_movie_URL = "https://casecomp.konnectrv.io/movie"
    r = requests.get(url = API_movie_URL)
    r = r.json()
    for item in r:
        movie = Movie()
        movie.title = item['title']
        movie.imdb = item['imdb']
        movie.date = item['release_date']
        movie.rate = item['rating']
        movie.platform = json.dumps(item['streaming_platform'])
        movie.companies = json.dumps(item['production_companies'])
        movie.vcount = item['vote_count']
        movie.v_average = str(item['vote_average'])
        movie.language = item['original_language']
        movie.popularity = str(item['popularity'])
        movie.overview = item['overview']
        movie.image_link = getMoviePoster(item['title'])
        movie.save()

def getComment(movie):
    global stopwords
    imdbID = movie.imdb
    # get the movie poster here, modify here
    response = requests.get(movie.image_link)
    colorArray = np.array(Image.open(BytesIO(response.content)))

    posterColor = ImageColorGenerator(colorArray)
    url = "https://www.imdb.com/title/" + imdbID + "/reviews?ref_=tt_urv"
    soup = BeautifulSoup(requests.get(url).text, features='lxml')
    comments = [a for a in soup.find_all("div", class_='text show-more__control')]
    length = max(25, len(comments))
    comments = comments[:length]
    commentsWithoutTag = [comment.get_text() for comment in comments]
    commentsStr = " ".join(commentsWithoutTag)
    wc = WordCloud(stopwords = stopwords, background_color="white", mask=colorArray).generate(commentsStr)
    plt.imshow(wc.recolor(color_func=posterColor), interpolation='bilinear')
    plt.axis("off")
    plt.savefig("crawler/static/crawler/resources/WordCloud/%s.jpg" % movie.index)


def downloadAllPics():
    movies = Movie.objects.all()


def getAllComments():
    movies = Movie.objects.all()
    for movie in movies:
        getComment(movie)

def alterField():
    movies = Movie.objects.all()
    for movie in movies:
        movie.comment_lists = 'crawler/resources/%s.jpg' % movie.index
        movie.save()

# createMovies()
# getAllComments()
# alterField()
# updateAllPictures()

def getAllGenre():
    movies = Movie.objects.all()
    for movie in movies:
        g = json.loads(movie.genre)
        # g = g.replace("[", "")
        # g = g.replace("]", "")
        # g = g.replace("'", "")
        # g = g.split(',')
        for genre in g:
            Genre.objects.get_or_create(genre=genre)

def updateAllGenre():
    movies = Movie.objects.all()
    for movie in movies:
        g = movie.genre
        g = g.replace("[", "")
        g = g.replace("]", "")
        g = g.replace("'", "")
        g = g.split(',')
        movie.genre = json.dumps(g)
        movie.save()

def getAllPlatforms():
    movies = Movie.objects.all()
    for movie in movies:
        g = json.loads(movie.platform)
        for platform in g:
            Platform.objects.get_or_create(platform=platform)

def getDictionary():
    # don't forget to change html5lib to other libraries

    # API_movie_URL = "https://casecomp.konnectrv.io/movie"
    # r = requests.get(url=API_movie_URL)
    # r = r.json()
    movies = Movie.objects.all()
    movieDictionary = {}
    count = 0

    for movie in movies:
        url = "https://www.imdb.com/title/" + movie.imdb
        soup = BeautifulSoup(requests.get(url).text, features='lxml')

        url = "https://www.imdb.com/title/" + movie.imdb + "/ratings"
        soup_rating = BeautifulSoup(requests.get(url).text, features='lxml')
        
        imdbdata = soup.find_all("script", type='application/ld+json')
        ratedata = [float(a.get_text().strip().strip("%")) * 0.01 for a in
                    soup_rating.find_all("div", {"class": "topAligned"})]
        # never do divisions

        dic = json.loads(imdbdata[0].get_text())

        # imdb data
        # movie.genre = dic['genre']
        # movieDictionary[i['title']]['posterURL'] = getMoviePoster(i['title'])
        # movieDictionary[i['title']]['imdb'] = i['imdb']
        movie.imdb_score= dic['aggregateRating']['ratingValue']
        movie.rate_data = ratedata  # percentage from voting point 10 to point 1
        movie.casts = json.dumps([a['name'] for a in dic['actor']])
        castURL = ["https://www.imdb.com" + a['url'] for a in dic['actor']]
        castImage = []
        for cast in castURL:
            soupCast = BeautifulSoup(requests.get(cast).text, features='lxml')
            urldata = soupCast.find_all("script", type='application/ld+json')
            castDic = json.loads(urldata[0].get_text())
            if 'image' in castDic:
                castImage.append(castDic['image'])
            else:
                castImage.append(None)

        movie.cast_image = json.dumps(castImage)

        # if 'image' in dic.keys():
        #     movieDictionary[i['title']]['posterURL'] = dic['image']
        # else:
        #     movieDictionary[i['title']]['posterURL'] = getMoviePoster(i['title'])
        print(count)
        count += 1
        movie.save()
    return movieDictionary


def getCommentCloudMap(movie):
    global stopwords

    imdbID = movie.imdb
    # get the movie poster here, modify here
    # response = requests.get(movie.image_link)
    # colorArray = np.array(Image.open(BytesIO(response.content)))
    # resp = urllib.urlopen(movie.image_link)
    # image = np.asarray(bytearray(resp.read(), dtype="uint8"))

    # get the movie poster here, modify here
    # colorArray = cv.imread(image)
    colorArray = cv.imread("crawler/static/crawler/resources/Poster/%s.jpg" % movie.index)
    posterColor = ImageColorGenerator(colorArray)

    imgray = cv.cvtColor(colorArray, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray, 127, 255, 0)
    maskArray, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    url = "https://www.imdb.com/title/" + imdbID + "/reviews?ref_=tt_urv"
    soup = BeautifulSoup(requests.get(url).text, features='lxml')
    comments = soup.find_all("div", class_='text show-more__control')
    length = max(25, len(comments))
    comments = comments[:length]
    commentsWithoutTag = [comment.get_text() for comment in comments]
    commentsStr = " ".join(commentsWithoutTag)

    wc = WordCloud(stopwords=stopwords, background_color="white", mask=maskArray, contour_width=3,
                   contour_color='firebrick').generate(commentsStr)

    plt.imshow(wc.recolor(color_func=posterColor), interpolation='bilinear')
    plt.axis("off")
    plt.savefig("crawler/static/crawler/resources/WordCloud/%s.jpg" % movie.index)

def getAllCommentsCloudMap():
    movies = Movie.objects.all()
    for movie in movies:
        getCommentCloudMap(movie)


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

def downloadPic(movie):
    img = requests.get(movie.image_link)
    with open('crawler/static/crawler/resources/Poster/%s.jpg' % movie.index, 'ab') as f:
        f.write(img.content)
        f.close()

def downloadAllPics():
    movies = Movie.objects.all()
    for movie in movies:
        downloadPic(movie)

# dictionaryTxt = json.loads(open('dic.txt', 'r').read())
comparisonFrame = 0
# result = getPercentageBetter(dictionaryTxt)
# print(result)
# getDictionary()
getAllCommentsCloudMap()
# downloadAllPics()

# getAllGenre()
# updateAllGenre()
# getAllPlatforms()