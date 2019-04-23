from django.conf.urls import url
from . import views

app_name = 'film'
urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^search/$', views.FilmDetails, name='film_details'),
]