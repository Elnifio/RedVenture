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
    # image_link = "https://www.bing.com/th?id=OIP.9BgnL75oBYrWpn7bZ069YwHaE8&pid=Api&rs=1"
    image_link = "https://www.bing.com/th?id=OIP.2_3PyPfpiv3Ke8zDx_PxFAHaJ4&w=137&h=183&c=7&o=5&dpr=2&pid=1.7"
    description = ""
    imdb = ""
    streaming_platform = ""
    production_companies = ["company 1", "company 2", "company 3"]
    rating = "R"
    title = "这里填充title"
    release_date = "Aug 28, 9102"
    original_language = ""
    popularity = ""

    return render(request, 'crawler/Search.html', {
        'message': message,
        "image": image_link,
        'title': title, 
        'date': release_date, 
        'companies': production_companies, 
        'rate': rating
        })

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