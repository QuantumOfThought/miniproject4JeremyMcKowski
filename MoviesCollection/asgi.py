### INF601 - Advanced Programming in Python
### Jeremy McKowski
### Mini Project 4

"""
ASGI config for MoviesCollection project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MoviesCollection.settings')

application = get_asgi_application()