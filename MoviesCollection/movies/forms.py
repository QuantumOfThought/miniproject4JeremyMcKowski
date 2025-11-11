### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4


from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ["title", "year", "genre", "director", "rating"]
