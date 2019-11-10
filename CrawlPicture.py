from bs4 import BeautifulSoup
import requests, json

def getMoviePoster(moviename = "Da Vinci Code"):
    url = "http://global.bing.com/images/search?q=" + moviename + " poster&qft=+filterui:imagesize-large&FORM=R5IR5"
    soup = BeautifulSoup(requests.get(url).text, features="html5lib")
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


dictionary = getDictionary()
print(dictionary)