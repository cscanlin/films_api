# Generated by Django 2.1.4 on 2018-12-19 03:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('url_slug', models.CharField(blank=True, max_length=255, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='films', to='films.Director')),
                ('related_films', models.ManyToManyField(blank=True, related_name='_film_related_films_+', to='films.Film')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='films.Film')),
            ],
        ),
    ]
