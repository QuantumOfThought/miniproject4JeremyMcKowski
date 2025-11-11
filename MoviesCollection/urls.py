### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

"""
URL configuration for MoviesCollection project.
Includes authentication and movie management routes.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from movies import views as movie_views
from accounts import views as account_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Main pages
    path('', movie_views.home, name='home'),
    path('movies/', include('movies.urls')),

    # Authentication
    path('auth/register/', account_views.register, name='register'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Profile
    path('profile/', account_views.profile, name='profile'),
]