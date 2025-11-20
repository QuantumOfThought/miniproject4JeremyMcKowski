### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Movie
from .forms import MovieForm, WatchlistForm



def home(request):
    """
    Home page showing recent movies from all users (public view).
    """
    movies = Movie.objects.all()[:10]  # Show latest 10 movies
    context = {
        'movies': movies,
        'total_movies': Movie.objects.count(),
        'page_title': 'Welcome to Movies Collection'
    }
    return render(request, 'movies/home.html', context)


@login_required
def my_movies(request):
    """
    Display current user's movie collection with search and filtering.
    """
    movies_list = Movie.objects.filter(owner=request.user)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        movies_list = movies_list.filter(
            Q(title__icontains=search_query) |
            Q(genre__icontains=search_query) |
            Q(director__icontains=search_query)
        )

    # Filter by rating
    rating_filter = request.GET.get('rating', '')
    if rating_filter:
        movies_list = movies_list.filter(rating=rating_filter)

    # Sort options
    sort_by = request.GET.get('sort', '-date_watched')
    valid_sorts = ['-date_watched', 'date_watched', 'title', '-title', 'rating', '-rating', 'year', '-year']
    if sort_by in valid_sorts:
        movies_list = movies_list.order_by(sort_by)

    # Pagination
    paginator = Paginator(movies_list, 12)  # 12 movies per page
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    context = {
        'movies': movies,
        'search_query': search_query,
        'rating_filter': rating_filter,
        'sort_by': sort_by,
        'page_title': 'My Movie Collection'
    }
    return render(request, 'movies/my_movies.html', context)


@login_required
def add_movie(request):
    """
    Add a new movie to user's collection.
    """
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.owner = request.user
            movie.save()
            messages.success(request, f'"{movie.title}" has been added to your collection!')
            return redirect('my_movies')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MovieForm()

    context = {
        'form': form,
        'page_title': 'Add New Movie',
        'form_title': 'Add Movie to Collection'
    }
    return render(request, 'movies/movie_form.html', context)


def movie_detail(request, pk):
    """
    Display detailed view of a single movie.
    """
    movie = get_object_or_404(Movie, pk=pk)

    # Check if current user owns this movie
    is_owner = request.user.is_authenticated and movie.owner == request.user

    context = {
        'movie': movie,
        'is_owner': is_owner,
        'page_title': f'{movie.title} ({movie.year})'
    }
    return render(request, 'movies/movie_detail.html', context)


@login_required
def edit_movie(request, pk):
    """
    Edit an existing movie (only by owner).
    """
    movie = get_object_or_404(Movie, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{movie.title}" has been updated successfully!')
            return redirect('movie_detail', pk=movie.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MovieForm(instance=movie)

    context = {
        'form': form,
        'movie': movie,
        'page_title': f'Edit {movie.title}',
        'form_title': f'Edit "{movie.title}"'
    }
    return render(request, 'movies/movie_form.html', context)


@login_required
def delete_movie(request, pk):
    """
    Delete a movie (only by owner) - handled via AJAX/modal.
    """
    movie = get_object_or_404(Movie, pk=pk, owner=request.user)

    if request.method == 'POST':
        title = movie.title
        movie.delete()
        messages.success(request, f'"{title}" has been deleted from your collection.')
        return redirect('my_movies')

    # If GET request, redirect to movie detail
    return redirect('movie_detail', pk=pk)


@login_required
def watchlist(request):
    """
    Display user's watchlist movies.
    """
    watchlist_movies = Movie.objects.filter(owner=request.user, is_watchlist=True)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        watchlist_movies = watchlist_movies.filter(
            Q(title__icontains=search_query) |
            Q(genre__icontains=search_query) |
            Q(director__icontains=search_query)
        )

    # Sort options
    sort_by = request.GET.get('sort', '-created_at')
    valid_sorts = ['-created_at', 'created_at', 'title', '-title', 'year', '-year']
    if sort_by in valid_sorts:
        watchlist_movies = watchlist_movies.order_by(sort_by)

    # Pagination
    paginator = Paginator(watchlist_movies, 12)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    context = {
        'movies': movies,
        'search_query': search_query,
        'sort_by': sort_by,
        'page_title': 'My Watchlist'
    }
    return render(request, 'movies/watchlist.html', context)


@login_required
def add_to_watchlist(request):
    """
    Add a movie to watchlist.
    """
    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.owner = request.user
            movie.is_watchlist = True
            movie.save()
            messages.success(request, f'"{movie.title}" has been added to your watchlist!')
            return redirect('watchlist')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = WatchlistForm()

    context = {
        'form': form,
        'page_title': 'Add to Watchlist',
        'form_title': 'Add Movie to Watchlist'
    }
    return render(request, 'movies/watchlist_form.html', context)


@login_required
def move_to_collection(request, pk):
    """
    Move a movie from watchlist to collection.
    """
    movie = get_object_or_404(Movie, pk=pk, owner=request.user, is_watchlist=True)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.is_watchlist = False
            movie.save()
            messages.success(request, f'"{movie.title}" has been moved to your collection!')
            return redirect('my_movies')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MovieForm(instance=movie)

    context = {
        'form': form,
        'movie': movie,
        'page_title': f'Move {movie.title} to Collection',
        'form_title': f'Complete details for "{movie.title}"'
    }
    return render(request, 'movies/movie_form.html', context)


@login_required
def dashboard(request):
    """
    Display user statistics dashboard.
    """
    user_movies = Movie.objects.filter(owner=request.user, is_watchlist=False)
    watchlist_movies = Movie.objects.filter(owner=request.user, is_watchlist=True)

    # Total statistics
    total_movies = user_movies.count()
    total_watchlist = watchlist_movies.count()

    # Genre breakdown
    genre_stats = user_movies.values('genre').annotate(
        count=models.Count('genre')
    ).order_by('-count')

    # Rating distribution
    rating_stats = user_movies.values('rating').annotate(
        count=models.Count('rating')
    ).order_by('rating')

    # Average rating
    avg_rating = user_movies.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0

    # Recent movies
    recent_movies = user_movies[:5]

    context = {
        'total_movies': total_movies,
        'total_watchlist': total_watchlist,
        'genre_stats': genre_stats,
        'rating_stats': rating_stats,
        'avg_rating': round(avg_rating, 1),
        'recent_movies': recent_movies,
        'page_title': 'Dashboard'
    }
    return render(request, 'movies/dashboard.html', context)