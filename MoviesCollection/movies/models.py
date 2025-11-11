### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Movie(models.Model):
    """
    Movie model for tracking personal movie collection.
    Each movie is associated with a user account.
    """

    # Basic movie information
    title = models.CharField(max_length=200, help_text="Movie title")
    year = models.PositiveIntegerField(help_text="Release year")
    genre = models.CharField(max_length=100, blank=True, help_text="Genre (e.g., Action, Comedy)")
    director = models.CharField(max_length=150, blank=True, help_text="Director name")

    # User interaction
    rating = models.IntegerField(
        choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(1, 6)],
        help_text="Your rating (1-5 stars)"
    )
    date_watched = models.DateField(help_text="When you watched it")
    notes = models.TextField(blank=True, help_text="Your thoughts about the movie")

    # User relationship
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_watched', '-created_at']
        verbose_name = "Movie"
        verbose_name_plural = "Movies"

    def __str__(self):
        return f"{self.title} ({self.year}) - {self.rating}/5 stars"

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'pk': self.pk})

    def get_star_display(self):
        """Return star rating as filled/empty stars"""
        filled_stars = '★' * self.rating
        empty_stars = '☆' * (5 - self.rating)
        return filled_stars + empty_stars