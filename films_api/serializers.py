from rest_framework import serializers

from .models import Film, Rating

class FilmSerializer(serializers.ModelSerializer):
    average_score = serializers.ReadOnlyField()

    class Meta:
        model = Film
        exclude = ('related_films',)

class RootFilmSerializer(FilmSerializer):
    related_films = FilmSerializer(many=True)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


# fields = ('title', 'description', 'url_slug', 'year', 'average_score')
