from rest_framework import serializers

from .models import Film, Rating

# The serializers controls which fields should be pulled from each model.

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    # Looks for `fields` in the query_params and removes any not listed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            fields_string = self.context['request'].query_params['fields']
        except KeyError:
            return
        for field_name in set(self.fields.keys()) - set(fields_string.split(',')):
            self.fields.pop(field_name)

class FilmSerializer(DynamicFieldsModelSerializer):
    # appropiately serialize average_score; see comment in api_controller on `FilmList`
    average_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Film
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'

class FilmRatingSerializer(serializers.ModelSerializer):
    # An extra serializer used for the `films/id/ratings/` route to exclude redundant data
    class Meta:
        model = Rating
        exclude = ('film',)

class RootFilmSerializer(FilmSerializer):
    # serializes each rating with redundant data removed
    ratings = FilmRatingSerializer(read_only=True, many=True, required=False)