from .models import Film
from .serializers import RootFilmSerializer
from rest_framework import generics, mixins
import django_filters
from django_filters.rest_framework import FilterSet, DjangoFilterBackend

class FilmFilter(FilterSet):
    min_year = django_filters.NumberFilter(name="year", lookup_expr='gte')
    max_year = django_filters.NumberFilter(name="year", lookup_expr='lte')

    class Meta:
        model = Film
        fields = ['min_year', 'max_year']

class FilmList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Film.objects.all()
    serializer_class = RootFilmSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = FilmFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class FilmDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Film.objects.all()
    serializer_class = RootFilmSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = FilmFilter

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
