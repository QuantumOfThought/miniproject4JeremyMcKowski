from django.shortcuts import render
from .models import Movie

def home(request):
    movies = Movie.objects.all()
    return render(request, "movies/home.html", {"movies": movies})

from django.shortcuts import render, redirect
from .forms import MovieForm

def add_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = MovieForm()
    return render(request, "movies/add.html", {"form": form})

from django.shortcuts import get_object_or_404

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect("home")

from django.shortcuts import get_object_or_404

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = MovieForm(instance=movie)
    return render(request, "movies/edit.html", {"form": form, "movie": movie})

