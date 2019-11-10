from django.http import HttpResponse
from django.shortcuts import render
from crawler.models import Movie

# Create your views here.
def getHomepage(request):
    movies = Movie.objects.all().order_by("-priority")[:5]
    return render(request, 'crawler/Homepage.html', {
        'movies': movies
    })

def search(request):
    request.encoding="utf-8"
    message = ""
    has_content = False
    if 'search' in request.GET and request.GET['search']:
        message = request.GET['search']
        print(request)
        has_content = True
    else:
            message = ""
            has_content = False
            return render(request, 'crawler/Search.html', {
                'has_content': has_content,
                'movie': None
            })
    # image_link = "https://www.bing.com/th?id=OIP.9BgnL75oBYrWpn7bZ069YwHaE8&pid=Api&rs=1"
    movie = Movie.objects.filter(imdb=message)
    if (len(movie) == 0):
        return render(request, 'crawler/Search.html', {
                'has_content': False,
                'movie': None
            })

    return render(request, 'crawler/Search.html', {
        'has_content': has_content,
        'movie': movie
        })

def getResultByIndex(request, index):
    movie = Movie.objects.filter(index=index)
    if len(movie) == 0:
        return render(request, 'crawler/Search.html', {
            'has_content': False,
            'movie': None
        })
    movie = movie[0]
    return render(request, 'crawler/Search.html', {
        'has_content': True,
        'movie': movie
    })

def getAllMovies(request):
    movies = Movie.objects.all().order_by("-priority")
    movies_obj = []
    i = 0
    while i < len(movies):
        movies_obj.append(movies[i:i+6])
        i += 5
    return render(request, 'crawler/AllMovies.html', {
        'movies': movies_obj
    })