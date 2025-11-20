### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_movie, name='add_movie'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('<int:pk>/edit/', views.edit_movie, name='edit_movie'),
    path('<int:pk>/delete/', views.delete_movie, name='delete_movie'),
    path('my-movies/', views.my_movies, name='my_movies'),

    # Watchlist URLs
    path('watchlist/', views.watchlist, name='watchlist'),
    path('watchlist/add/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/<int:pk>/move/', views.move_to_collection, name='move_to_collection'),

    # Dashboard URL
    path('dashboard/', views.dashboard, name='dashboard'),
]