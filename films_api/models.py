import os
import json
from django.db import models

from django.conf import settings
from django.forms.models import model_to_dict

class Film(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    url_slug = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    related_films = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.title

    @classmethod
    def load_from_file(cls, filename=os.path.join(settings.BASE_DIR, 'films.json')):
        with open(filename) as f:
            for film_data in json.load(f)['films']:
                related_film_ids = film_data.pop('related_film_ids', [])
                film, _ = cls.objects.get_or_create(pk=film_data['id'])
                for k, v in film_data.items():
                    setattr(film, k, v)
                film.related_films.add(*(cls.objects.get_or_create(pk=rel_id)[0] for rel_id in related_film_ids))
                film.save()

    def serialize(self, exclude={'related_films'}):
        return {
            'film': model_to_dict(self, exclude=exclude),
            'related_films': [model_to_dict(related, exclude=exclude) for related in self.related_films.all()],
        }
