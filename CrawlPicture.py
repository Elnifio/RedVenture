from bs4 import BeautifulSoup
import requests, json
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def getMoviePoster(moviename):
    url = "http://global.bing.com/images/search?q=" + moviename + " poster&qft=+filterui:imagesize-large&FORM=R5IR5"
    soup = BeautifulSoup(requests.get(url).text, features="html5lib")
    images = [a["src"] for a in soup.find_all("img", {"alt": " "})]
    poster = images[0]
    poster = poster.replace("&", "&amp")
    return poster

def getDictionary():
    API_movie_URL = "https://casecomp.konnectrv.io/movie"
    r = requests.get(url=API_movie_URL)
    r = r.json()
    movieDictionary = {}

    for i in r:
        url = "https://www.imdb.com/title/" + i['imdb']
        soup = BeautifulSoup(requests.get(url).text, features='html5lib')
        genre = [a for a in soup.find_all("script", type='application/ld+json')]
        dic = json.loads(genre[0].get_text())
        movieDictionary[i['title']] = {}
        movieDictionary[i['title']]["release_date"] = i['release_date']
        movieDictionary[i['title']]['rating'] = i['rating']
        movieDictionary[i['title']]['streaming_platform'] = i['streaming_platform']
        movieDictionary[i['title']]['production_companies'] = i['production_companies']
        movieDictionary[i['title']]['overview'] = i['overview']
        movieDictionary[i['title']]['posterURL'] = getMoviePoster(i['title'])
        movieDictionary[i['title']]['imdb'] = i['imdb']
        movieDictionary[i['title']]['genre'] = dic['genre']
        if 'image' in dic.keys():
            movieDictionary[i['title']]['posterURL'] = dic['image']
        else:
            movieDictionary[i['title']]['posterURL'] = getMoviePoster(i['title'])
    return movieDictionary


def getComment(movieName):
    global stopwords
    imdbID = "tt4633694"
    # get the movie poster here, modify here
    colorArray = np.array(Image.open("th.jpeg"))

    posterColor = ImageColorGenerator(colorArray)
    url = "https://www.imdb.com/title/" + imdbID + "/reviews?ref_=tt_urv"
    soup = BeautifulSoup(requests.get(url).text, features='html5lib')
    comments = [a for a in soup.find_all("div", class_='text show-more__control')]
    length = max(25, len(comments))
    comments = comments[:length]
    commentsWithoutTag = [comment.get_text() for comment in comments]
    commentsStr = " ".join(commentsWithoutTag)
    wc = WordCloud(stopwords = stopwords, background_color="white", mask=colorArray).generate(commentsStr)
    plt.imshow(wc.recolor(color_func=posterColor), interpolation='bilinear')
    plt.axis("off")
    plt.show()


dictionary = getDictionary()
stopwords = set(STOPWORDS)
stopwords.update(["movie", "film", "series", "show", "done", "watch", "see", "us", "story", "scene", "many"])