from django.http import HttpResponse
from django.shortcuts import render
from crawler.models import Movie, Genre, Platform

# Create your views here.
def getHomepage(request):
    priority_movies = Movie.objects.all().order_by("-priority")[:5]
    trending_movies = Movie.objects.all().order_by("-date")[:5]
    genres = Genre.objects.all()[:6]
    platforms = Platform.objects.all()[:6]
    return render(request, 'crawler/Homepage.html', {
        'priority_movies': priority_movies, 
        'trending_movies': trending_movies, 
        'genres': genres, 
        'pfs': platforms
    })

def search(request):
    request.encoding="utf-8"
    message = ""
    has_content = False
    if 'search' in request.GET and request.GET['search']:
        message = request.GET['search']
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
        'movie': movie[0]
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

def getAllMoviesByPriority(request):
    movies = Movie.objects.all().order_by("-priority")
    movies_obj = []
    i = 0
    while i < len(movies):
        movies_obj.append(movies[i:i+6])
        i += 5
    return render(request, 'crawler/AllMovies.html', {
        'movies': movies_obj, 
        'title': "All Trending Movies"
    })

def getAllMoviesByDatetime(request):
    movies = Movie.objects.all().order_by("-date")
    movies_obj = []
    i = 0
    while i < len(movies):
        movies_obj.append(movies[i:i+6])
        i += 6
    return render(request, 'crawler/AllMovies.html', {
        'movies': movies_obj, 
        'title': "Most Recent Movies"
    })

def getAllMoviesByGenre(request, genre):
    out = Movie.objects.filter(genre__icontains=genre)
    out_obj = []
    i = 0
    while i < len(out):
        out_obj.append(out[i:i+6])
        i += 6
    return render(request, 'crawler/AllMovies.html', {
        'movies': out_obj,
        'title': genre
    })

def getAllMoviesByPlatform(request, pf):
    out = Movie.objects.filter(platform__icontains=pf)
    out_obj = []
    i = 0
    while i < len(out):
        out_obj.append(out[i:i+6])
        i += 6
    return render(request, 'crawler/AllMovies.html', {
        'movies': out_obj,
        'title': pf
    })

def getAllCategories(request):
    genres = Genre.objects.all()
    i = 0
    out = []
    while i < len(genres):
        out.append(genres[i:i+6])
        i += 6
    return render(request, 'crawler/AllGenres.html', {
        'genres': out,
        'title': 'All Genres'
    })

def getAllPlatforms(request):
    genres = Platform.objects.all()
    i = 0
    out = []
    while i < len(genres):
        out.append(genres[i:i+6])
        i += 6
    return render(request, 'crawler/AllPlatforms.html', {
        'pfs': out,
        'title': 'All Platforms'
    })