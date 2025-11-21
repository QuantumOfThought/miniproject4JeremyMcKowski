### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import models  # ADD THIS LINE
from .models import Movie
from .forms import MovieForm, WatchlistForm


def register(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
        'page_title': 'Create Account'
    }
    return render(request, 'accounts/register.html', context)


@login_required
def profile(request):
    """
    User profile view showing account info and movie statistics.
    """
    user = request.user
    movies = user.movies.all()

    # Calculate statistics
    total_movies = movies.count()
    avg_rating = movies.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
    favorite_genres = movies.values('genre').annotate(
        count=models.Count('genre')
    ).order_by('-count')[:5]

    recent_movies = movies[:5]

    context = {
        'user': user,
        'total_movies': total_movies,
        'avg_rating': round(avg_rating, 1),
        'favorite_genres': favorite_genres,
        'recent_movies': recent_movies,
        'page_title': f'{user.username}\'s Profile'
    }
    return render(request, 'accounts/profile.html', context)