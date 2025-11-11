### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

from django import forms
from .models import Movie
from datetime import date


class MovieForm(forms.ModelForm):
    """
    Enhanced form for adding/editing movies with Bootstrap styling and validation.
    """

    class Meta:
        model = Movie
        fields = ['title', 'year', 'genre', 'director', 'rating', 'date_watched', 'notes']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter movie title',
                'required': True
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Release year (e.g., 2023)',
                'min': 1900,
                'max': date.today().year + 5,
                'required': True
            }),
            'genre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Genre (e.g., Action, Comedy, Drama)',
            }),
            'director': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Director name',
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'date_watched': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What did you think about this movie?',
                'rows': 4
            })
        }

        labels = {
            'title': 'Movie Title',
            'year': 'Release Year',
            'genre': 'Genre',
            'director': 'Director',
            'rating': 'Your Rating',
            'date_watched': 'Date Watched',
            'notes': 'Your Review/Notes'
        }

    def clean_year(self):
        """Validate year is reasonable"""
        year = self.cleaned_data.get('year')
        current_year = date.today().year

        if year and (year < 1900 or year > current_year + 5):
            raise forms.ValidationError(f"Year must be between 1900 and {current_year + 5}")

        return year

    def clean_date_watched(self):
        """Validate date watched is not in future"""
        date_watched = self.cleaned_data.get('date_watched')

        if date_watched and date_watched > date.today():
            raise forms.ValidationError("Date watched cannot be in the future")

        return date_watched