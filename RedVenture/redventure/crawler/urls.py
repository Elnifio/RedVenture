from django.urls import path, include

import crawler.views

urlpatterns = [
    path("", crawler.views.getHomepage), 
    path("search", crawler.views.search),
    path("movie/<int:index>", crawler.views.getResultByIndex), 
    path("popular_movies", crawler.views.getAllMoviesByPriority), 
    path("recent_movies", crawler.views.getAllMoviesByDatetime),
    path("category/<str:genre>", crawler.views.getAllMoviesByGenre), 
    path("category", crawler.views.getAllCategories),
    path("platform", crawler.views.getAllPlatforms),
    path("platform/<str:pf>", crawler.views.getAllMoviesByPlatform)
]