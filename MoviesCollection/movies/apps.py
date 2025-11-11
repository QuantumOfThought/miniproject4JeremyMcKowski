### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

from django.apps import AppConfig

class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = "Movie Collection"