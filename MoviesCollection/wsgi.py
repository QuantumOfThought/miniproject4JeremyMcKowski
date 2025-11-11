### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

"""
WSGI config for MoviesCollection project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MoviesCollection.settings')

application = get_wsgi_application()