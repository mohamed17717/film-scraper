from django.db import models
from django.shortcuts import reverse


# Create your models here.
class FilmInformation(models.Model):
    ''' This Table contain Film Information in FilmInformationorary
    in other words data is not trusted it might be wrong '''

        ## film info
    name     = models.CharField(max_length=70, unique= True)
    year     = models.CharField(max_length=4)
        ## all next can be null
    mpaa     = models.CharField(blank=True, null=True, max_length=20)
    length   = models.CharField(blank=True, null=True, max_length=20)
    category = models.CharField(blank=True, null=True, max_length=60)
    poster   = models.URLField (blank=True, null=True, max_length=200) 
    trailer  = models.URLField (blank=True, null=True, max_length=200)
    brief_en = models.TextField(blank=True, null=True)
    brief_ar = models.TextField(blank=True, null=True)
    country  = models.CharField(blank=True, null=True, max_length=50)
    language = models.CharField(blank=True, null=True, max_length=50)
        ## saved as text json data
    rating   = models.TextField(blank=True, null=True)
    reviews  = models.TextField(blank=True, null=True)
    cast     = models.TextField(blank=True, null=True)
    torrent  = models.TextField(blank=True, null=True)
    download = models.TextField(blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    prizes_won = models.TextField(blank=True, null=True)
    prizes_nomenee = models.TextField(blank=True, null=True)

    ## data to help
    trust    = models.BooleanField(default= False)
    trusted  = models.IntegerField(default= 0)

    ## json
    json = models.TextField(null=True, blank=True)

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'FilmInformation'
        verbose_name_plural = 'FilmInformations'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("film", kwargs={"name": self.name})
