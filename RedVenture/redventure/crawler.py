from bs4 import BeautifulSoup
import requests, json
import django, os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redventure.settings')
django.setup()
stopwords = set(STOPWORDS)
stopwords.update(["movie", "film", "series", "show", "done", "watch", "see", "us", "story", "scene", "many"])

from crawler.models import Movie

def getMoviePoster(moviename = "Da Vinci Code"):
    url = "http://global.bing.com/images/search?q=" + moviename + " poster&qft=+filterui:imagesize-large&FORM=R5IR5"
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    images = [a["src"] for a in soup.find_all("img", {"alt": " "})]
    poster = images[0]
    poster = poster.replace("&", "&amp")
    return poster

def getDictionary():
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
        movie.genre = dic['genre']
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
    plt.savefig("crawler/static/crawler/resources/%s.jpg" % movie.index)


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
getAllComments()
# alterField()
# updateAllPictures()
