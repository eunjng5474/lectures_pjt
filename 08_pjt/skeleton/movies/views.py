from django.shortcuts import render
from django.views.decorators.http import require_safe
from .models import Genre, Movie
from rest_framework.decorators import api_view


# Create your views here.
@require_safe
@api_view(['GET'])
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    genre = movie.genres.all()
    context = {
        'movie': movie,
        'genres': genre,
    }
    return render(request, 'movies/detail.html', context)


@require_safe
def recommended(request):
    movies = Movie.objects.all().order_by('-vote_average', '-popularity')[:10]
    context = {
        'movies': movies,
    }
    return render(request, 'movies/recommended.html', context)
