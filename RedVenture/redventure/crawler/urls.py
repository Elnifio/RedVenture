from django.urls import path, include

import crawler.views

urlpatterns = [
    path("", crawler.views.getHomepage), 
    path("search", crawler.views.search),
    path("movie/<int:index>", crawler.views.getResultByIndex), 
    path("all_movie", crawler.views.getAllMovies)
]