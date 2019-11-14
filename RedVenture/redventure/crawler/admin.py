from django.contrib import admin
from .models import Movie, Page, Genre, Platform
# Register your models here.
admin.site.register(Movie)
admin.site.register(Page)
admin.site.register(Genre)
admin.site.register(Platform)