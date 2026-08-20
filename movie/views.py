from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

# Create your views here.

def home(request):
    # código HTML en views :(
    # return HttpResponse('<h1>Welcome to Home Page</h1>')
    
    #uso de plantilla sin parámetros
    #return render(request, 'home.html')

    # uso de plantilla con parámetros
    #return render(request, 'home.html', {'name':'Paola Vallejo'})

    # búsqueda de películas
    searchTerm = request.GET.get('searchMovie')

    # si se está buscando una película
    if searchTerm:
        # lista únicamente la(s) película(s) cuyo título contiene el nombre buscado
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else: 
        # lista todas las películas de la base de datos
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})



 # Función para 'About'
def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
   
    #uso de plantilla sin parámetros
    return render(request, 'about.html')