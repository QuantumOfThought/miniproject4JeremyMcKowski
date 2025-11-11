from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "genre", "director", "rating", "created_at")
    search_fields = ("title", "genre", "director")
    list_filter = ("genre", "year")
    ordering = ("-created_at",)
