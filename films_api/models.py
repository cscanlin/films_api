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
    img_url = models.CharField(max_length=10000, null=True, blank=True)

    # many to many related with itself. There is a hidden through table
    # related_films = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.title

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

### users

import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from proj_common.utils.auth_utils.external_storage import RedisCommonStorage


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='User public identifier')


def user_avatar_path(instance, filename):
    # file will be uploaded to media/user_avatar/<id>/<filename> TODO: why media_root not work ... ?
    return 'media/user_avatar/{0}/{1}'.format(instance.user.uuid, filename)


class Profile(models.Model):
    # TODO: maybe extra uuid for profile can be useful but not now
    # user_profile_uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4,
    #                                       verbose_name='User profile public identifier')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    images_json = JSONField(help_text='avatar', blank=True, default=dict)
    details_json = JSONField(help_text='location, sex, date of birth', blank=True, default=dict)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        profile = instance.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=instance)
    else:
        profile = instance.profile
    finally:
        profile.save()

    #Delete tocken after user profile updated
    RedisCommonStorage().cache.delete('redis-common-storage.{}'.format(profile.user.uuid))

