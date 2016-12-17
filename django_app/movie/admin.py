from django.contrib import admin
from movie.models import Movie, Actor, Director, Genre, Nation

admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Nation)
