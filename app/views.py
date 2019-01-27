from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from json import dumps, loads
from .scripts.scrape_film import Film

from .models import FilmInformation

# Create your views here.
def Home(request):
    return render(request, 'home.html', {})

def get_object(Class, **kwargs):
    try:
        return Class.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None

def FilmDetails(request):
    if request.method == 'POST':
        filmName = request.POST.get('q')
        if filmName:
            info = get_object(FilmInformation, name=filmName.title())
            if not info:
                f = Film(filmName)
                f.build()
                info = f.info
                info.pop('user-query')
                info.update({'json': dumps(info)})
                film = FilmInformation(**info)
                film.save()
            else:
                info = loads(info.json)
            return render(request, 'details.html', info)
            # return HttpResponse( dumps(info.__dict__), content_type='application/json' )
            # return HttpResponse(info.__dict__)
        return HttpResponse('no filmName')
    return HttpResponse('no post')
        

 