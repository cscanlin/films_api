# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 10:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('films_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='films_api.Film')),
            ],
        ),
    ]
