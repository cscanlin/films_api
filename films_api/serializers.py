from rest_framework import serializers

from .models import Film

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        exclude = ('related_films',)

class RootFilmSerializer(FilmSerializer):
    related_films = FilmSerializer(many=True)
