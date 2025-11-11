### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Movie model with better organization and filtering.
    """

    # List display
    list_display = ['title', 'year', 'genre', 'director', 'rating', 'owner', 'date_watched', 'created_at']

    # Filters
    list_filter = ['genre', 'year', 'rating', 'date_watched', 'owner']

    # Search
    search_fields = ['title', 'director', 'genre', 'owner__username']

    # Ordering
    ordering = ['-date_watched', '-created_at']

    # Form organization
    fieldsets = (
        ('Movie Information', {
            'fields': ('title', 'year', 'genre', 'director')
        }),
        ('Your Review', {
            'fields': ('rating', 'date_watched', 'notes')
        }),
        ('Owner', {
            'fields': ('owner',)
        }),
    )

    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']

    # Pagination
    list_per_page = 25

    # Date hierarchy
    date_hierarchy = 'date_watched'

    def get_queryset(self, request):
        """
        Limit queryset to movies owned by current user (unless superuser).
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        """
        Automatically set the owner to current user when creating new movies.
        """
        if not change:  # If creating new object
            obj.owner = request.user
        super().save_model(request, obj, form, change)


# Customize admin site headers
admin.site.site_header = "Movies Collection Admin"
admin.site.site_title = "Movies Collection"
admin.site.index_title = "Manage Your Movie Collection"