from rest_framework import serializers

from .models import Film, Rating

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            fields_string = self.context['request'].query_params['fields']
        except KeyError:
            return
        for field_name in set(self.fields.keys()) - set(fields_string.split(',')):
            self.fields.pop(field_name)

class FilmSerializer(DynamicFieldsModelSerializer):
    average_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Film
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = '__all__'

class FilmRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ('film',)

class RootFilmSerializer(FilmSerializer):
    ratings = FilmRatingSerializer(many=True, required=False)
