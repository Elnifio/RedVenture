from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def getHomepage(request):
    return render(request, 'crawler/Homepage.html', {})

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
    image_link = ""
    description = ""
    imdb = ""
    streaming_platform = ""
    production_companies = ""
    rating = ""
    title = ""
    release_date = ""
    original_language = ""
    popularity = ""

    return render(request, 'crawler/Search.html', {'message': message})

def getResultByIMDB(imdb):
    image_link = ""
    description = ""
    streaming_platform = ""
    production_companies = ""
    rating = ""
    title = ""
    release_date = ""
    original_language = ""
    popularity = ""
    return ({
        'img': image_link, 
        'desc': description, 
        'platform': streaming_platform,
        'companies': production_companies,
        'rate': rating,
        'date': release_date,
        'title': title,
        'lang': original_language, 
        'popularity': popularity
    })