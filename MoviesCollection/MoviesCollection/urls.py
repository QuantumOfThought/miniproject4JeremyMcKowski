### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4


from django.contrib import admin
from django.urls import path
from movies import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("add/", views.add_movie, name="add_movie"),
    path("delete/<int:movie_id>/", views.delete_movie, name="delete_movie"),
    path("edit/<int:movie_id>/", views.edit_movie, name="edit_movie"),
]
