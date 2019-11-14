from django.http import HttpResponse
from django.shortcuts import render
from crawler.models import Movie, Genre, Platform, Page

# Create your views here.
def getHomepage(request):
    priority_movies = Movie.objects.all().order_by("-priority")[:5]
    trending_movies = Movie.objects.all().order_by("-date")[:5]
    genres = Genre.objects.all()[:6]
    platforms = Platform.objects.all()[:6]
    Page.objects.get(title='Homepage').auto_increment()
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
    Page.objects.get(title="Search").auto_increment()
    if 'search' in request.GET and request.GET['search']:
        message = request.GET['search']
        has_content = True
    else:
            message = ""
            return render(request, 'crawler/Search.html', {
                'has_content': False,
                'movie': None,
                'search': ""
            })
    movie = Movie.objects.filter(title__icontains=message)
    movie = movie.union(Movie.objects.filter(imdb__icontains=message))
    search = message
    message = message.split(" ")
    for item in message:
        movie = movie.union(Movie.objects.filter(title__icontains=item))
    if (len(movie) == 0):
        return render(request, 'crawler/SearchResult.html', {
                'has_content': False,
                'results': None,
                'search': search
            })

    return render(request, 'crawler/SearchResult.html', {
        'has_content': has_content,
        'results': movie, 
        'search': search
        })

def getResultByIndex(request, index):
    movie = Movie.objects.filter(index=index)
    Page.objects.get(title="Search").auto_increment()
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
    Page.objects.get(title="Popular").auto_increment()
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
    Page.objects.get(title="Trending").auto_increment()
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
    Genre.objects.get(genre=genre).auto_increment()
    Page.objects.get(title="Genres").auto_increment()
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
    Platform.objects.get(platform=pf).auto_increment()
    Page.objects.get(title="Platforms").auto_increment()
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
    Page.objects.get(title="Genres").auto_increment()
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
    Page.objects.get(title="Platforms").auto_increment()
    while i < len(genres):
        out.append(genres[i:i+6])
        i += 6
    return render(request, 'crawler/AllPlatforms.html', {
        'pfs': out,
        'title': 'All Platforms'
    })

def getPagesStatistics(request):
    pages = Page.objects.all().order_by("-counter")
    return render(request, 'crawler/PageStat.html', {
        'pages': pages
    })

def getMovieStats(request):
    movies = Movie.objects.all().order_by("-priority")
    return render(request, 'crawler/MovieStat.html', {
        'objects': movies,
        'category': "Movies"
    })

def getPlatformStats(request):
    platforms = Platform.objects.all().order_by("-priority")
    return render(request, 'crawler/PfGenreStat.html', {
        'objects': platforms,
        "category": "Platform"
    })

def getGenreStats(request):
    genres = Genre.objects.all().order_by("-priority")
    return render(request, 'crawler/PfGenreStat.html', {
        'objects': genres,
        'category': "Genre"
    })