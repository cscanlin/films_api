import os
import json
import statistics

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Film(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    # many to many related with itself. There is a hidden through table
    related_films = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.title

    @classmethod
    def load_from_file(cls, filename=os.path.join(settings.BASE_DIR, 'films.json')):
        # loads data from sample file. (could be made more efficient)
        with open(filename) as f:
            for film_data in json.load(f)['films']:
                related_film_ids = film_data.pop('related_film_ids', [])
                film, _ = cls.objects.get_or_create(pk=film_data['id'])
                for k, v in film_data.items():
                    setattr(film, k, v)
                film.related_films.add(*(cls.objects.get_or_create(pk=rel_id)[0] for rel_id in related_film_ids))
                film.save()

    @property
    def _average_score(self):
        # favor `query.annotate(average_score=Avg('ratings__score'))`
        try:
            return statistics.mean(rating.score for rating in self.ratings.all())
        except statistics.StatisticsError:
            return 0

class Rating(models.Model):
    film = models.ForeignKey(Film, related_name='ratings')
    score = models.IntegerField(validators=[
        MinValueValidator(0),
        MaxValueValidator(10),
    ])
