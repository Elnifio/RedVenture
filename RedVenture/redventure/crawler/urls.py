from django.urls import path, include

import crawler.views

urlpatterns = [
    path("", crawler.views.getHomepage), 
    path("search", crawler.views.search)
]