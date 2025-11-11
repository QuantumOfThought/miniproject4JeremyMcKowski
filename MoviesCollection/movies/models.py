### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=100, blank=True)
    director = models.CharField(max_length=150, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)  # e.g., 7.8
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        yr = f" ({self.year})" if self.year else ""
        return f"{self.title}{yr}"
