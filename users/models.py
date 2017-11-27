import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='User public identifier')
