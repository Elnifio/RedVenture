from django.db import models
import json

# Create your models here.
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

    def getPlatform(self):
        return json.loads(self.platform)
    
    def getCompanies(self):
        return json.loads(self.companies)
    
    def increment(self):
        self.priority += 1
        self.save()
        return

    def __str__(self):
        return "(%s) %s: %s" % (self.index, self.title, self.imdb)