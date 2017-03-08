from .models import Film, Rating
from .serializers import RootFilmSerializer, RatingSerializer
from rest_framework import generics
import django_filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend

class FilmFilter(FilterSet):
    min_year = django_filters.NumberFilter(name="year", lookup_expr='gte')
    max_year = django_filters.NumberFilter(name="year", lookup_expr='lte')
    title = django_filters.CharFilter(name="title", lookup_expr='icontains')
    description = django_filters.CharFilter(name="description", lookup_expr='icontains')

    class Meta:
        model = Film
        fields = ['min_year', 'max_year', 'title', 'description']

class FilmList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = RootFilmSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = FilmFilter

class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = RootFilmSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = FilmFilter

class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
