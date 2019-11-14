from django.db import models
import json
import re

# Create your models here.

class Page(models.Model):
    index = models.AutoField(primary_key=True)
    title = models.TextField(default="NewPage")
    counter = models.IntegerField(default=0)

    def auto_increment(self):
        self.counter += 1
        self.save()
        return
    
    def __str__(self):
        return "%s: %s" % (self.title, self.counter)


class Genre(models.Model):
    index = models.AutoField(primary_key=True)
    genre = models.TextField(default="")
    priority = models.IntegerField(default=0)
    
    def auto_increment(self):
        self.priority += 1
        self.save()

    def __str__(self):
        return "(%s) %s" % (self.index, self.genre)
    
    def name(self):
        return self.genre


class Platform(models.Model):
    index = models.AutoField(primary_key=True)
    platform = models.TextField(default="")
    priority = models.IntegerField(default=0)

    def auto_increment(self):
        self.priority += 1
        self.save()

    def __str__(self):
        return "(%s) %s" % (self.index, self.platform)
    
    def name(self):
        return self.platform


class Movie(models.Model):
    index = models.AutoField(primary_key=True)
    title = models.TextField()
    imdb = models.TextField()
    date = models.TextField()
    rate = models.TextField()
    platform = models.TextField(default="[]")
    companies = models.TextField(default="[]")
    vcount = models.IntegerField()
    v_average = models.TextField()
    language = models.TextField()
    popularity = models.TextField()
    overview = models.TextField()
    image_link = models.TextField()
    priority = models.IntegerField(default=0)
    comment_lists = models.TextField(default="crawler/resources/%s.jpg" % index)
    genre = models.TextField(default="")
    date_time = models.IntegerField(default=0)
    imdb_score = models.TextField(default="")
    rate_data = models.TextField(default="")
    casts = models.TextField(default="")
    cast_image = models.TextField(default="")
    genreBetterPercentage = models.TextField(default="")
    allBetterPercentage = models.TextField(default="")

    def getGenrePercentage(self):
        return "{:.2f}%".format(float(self.genreBetterPercentage) * 100)

    def getAllPercentage(self):
        return "{:.2f}%".format(float(self.allBetterPercentage) * 100)

    def getVote(self):
        return float(self.v_average)

    def getIMDB(self):
        return float(self.imdb_score)
    
    def getVotePercentage(self):
        return "%s%%" % (self.getVote() * 10)

    def getRemainingPercentage(self):
        return "%s%%" % (100 - self.getVote() * 10)

    def getGenre(self):
        return json.loads(self.genre)
        
    def getCasts(self):
        return json.loads(self.casts)

    def getCastImages(self):
        return json.loads(self.cast_image)

    def getPlatform(self):
        return json.loads(self.platform)
    
    def getCompanies(self):
        return json.loads(self.companies)
    
    def increment(self):
        self.priority += 1
        self.save()
        return

    def getYear(self):
        return self.date[:4]

    def getLink(self, platform):
        if (platform == 'netflix'):
            return 'https://www.netflix.com' 
        elif (platform == 'hbo'):
            return 'https://www.hbo.com'
        elif (platform == 'amazon_prime'):
            return 'https://www.primevideo.com'

    def __str__(self):
        return "(%s) %s: %s" % (self.index, self.title, self.imdb)

    def name(self):
        return self.title
