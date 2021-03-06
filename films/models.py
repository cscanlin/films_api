import statistics

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

class Director(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def relations_diplay_fields(cls):
        return {
            'films': 'title',
        }

    @classmethod
    def calculated_properties(cls):
        return {
            'average_score': (models.FloatField, Avg('films__ratings__score')),
        }

class Film(models.Model):

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    url_slug = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    director = models.ForeignKey(Director, related_name='films', on_delete=models.CASCADE)

    # many to many related with itself. There is a hidden through table
    related_films = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.title

    @classmethod
    def relations_diplay_fields(cls):
        return {
            'director': 'name',
            'ratings': 'score',
            'related_films': 'title',
        }

    @classmethod
    def calculated_properties(cls):
        return {
            'average_score': (models.FloatField, Avg('ratings__score')),
        }

    @property
    def _average_score(self):
        # favor `query.annotate(average_score=Avg('ratings__score'))`
        try:
            return statistics.mean(rating.score for rating in self.ratings.all())
        except statistics.StatisticsError:
            return 0

class Rating(models.Model):
    film = models.ForeignKey(Film, related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(10),
    ])

    def __str__(self):
        return str(self.score)

    @classmethod
    def relations_diplay_fields(cls):
        return {
            'film': 'title',
        }
