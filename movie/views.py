from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64


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


def render_bar_chart(counts, title, xlabel):
    """Genera un gráfico de barras y lo devuelve como string base64."""
    plt.figure(figsize=(10, 6))

    positions = range(len(counts))
    plt.bar(positions, counts.values(), width=0.5, align='center')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Number of movies')
    plt.xticks(positions, counts.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()

    return base64.b64encode(image_png).decode('utf-8')


def statistics_view(request):
    all_movies = Movie.objects.all()

    # --- Conteo por año ---
    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else 'None'
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    # --- Conteo por primer género ---
    movie_counts_by_genre = {}
    for movie in all_movies:
        raw_genre = (movie.genre or '').strip()
        first_genre = raw_genre.split(',')[0].strip() if raw_genre else 'None'
        movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    # Ordenamientos
    movie_counts_by_year = dict(sorted(movie_counts_by_year.items(), key=lambda i: str(i[0])))
    movie_counts_by_genre = dict(
        sorted(movie_counts_by_genre.items(), key=lambda i: i[1], reverse=True)
    )

    # --- Generación de las dos gráficas ---
    graphic_year = render_bar_chart(movie_counts_by_year, 'Movies per year', 'Year')
    graphic_genre = render_bar_chart(movie_counts_by_genre, 'Movies per genre', 'Genre')

    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre,
    })