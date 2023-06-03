from django.shortcuts import render, redirect
from .models import Movie, Comment
from .forms import MovieForm, CommentForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe


# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movies/index.html', context)

@require_http_methods(['GET', 'POST'])
def create(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = MovieForm(request.POST, request.FILES)
            if form.is_valid():
                movie = form.save(commit=False)
                movie.user = request.user
                movie.save()
                return redirect('movies:detail', movie.pk)
        else:
            form = MovieForm()
        
        context = {'form': form}
        return render(request, 'movies/create.html', context)
    else:
        return redirect('movies:index')
    
@require_safe
def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    context = {
        'movie':movie,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'movies/detail.html', context)

@require_http_methods(['GET', 'POST'])
def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', pk=movie.pk)
        else:
            form = MovieForm(instance=movie)
        
        context = {
            'form':form,
            'movie':movie
        }
        return render(request, 'movies/update.html', context)
    return redirect('movies:detail', pk=movie.pk)
        

@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=pk)
        if request.user == movie.user:
            movie.delete()
    return redirect('movies:index')

@require_POST
def comment_create(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
    return redirect('movies:detail', movie.pk)

@require_POST
def comment_delete(request, movie_pk, comment_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('movies:detail', movie_pk)


@require_POST
def likes(request, movie_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return redirect('movies:index')
    return redirect('accounts:login')

@require_POST
def dislikes(request, movie_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=movie_pk)
        if movie.dislike_users.filter(pk=request.user.pk).exists():
            movie.dislike_users.remove(request.user)
        else:
            movie.dislike_users.add(request.user)
        return redirect('movies:index')
    return redirect('accounts:login')