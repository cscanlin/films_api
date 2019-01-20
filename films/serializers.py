from rest_framework import serializers

from db_table.serializers import DynamicFieldsModelSerializer

from .models import Film, Rating

# The serializers controls which fields should be pulled from each model.

class FilmSerializer(DynamicFieldsModelSerializer):
    # appropiately serialize average_score; see comment in views on `FilmList`
    average_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Film
        fields = '__all__'

class RatingSerializer(DynamicFieldsModelSerializer):
    film = FilmSerializer(read_only=True, required=False)

    class Meta:
        model = Rating
        fields = '__all__'

class FilmRatingSerializer(DynamicFieldsModelSerializer):
    # An extra serializer used for the `films/id/ratings/` route to exclude redundant data
    class Meta:
        model = Rating
        exclude = ('film',)

class RootFilmSerializer(FilmSerializer):
    ratings = FilmRatingSerializer(read_only=True, many=True, required=False)
    related_films = FilmSerializer(read_only=True, many=True, required=False)
