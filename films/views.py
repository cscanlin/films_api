from django.db.models import Avg
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import generics, mixins, filters, status
from rest_framework.response import Response

from auto_drf.auto_filters import dynamic_field_filters

from .models import Film, Rating
from .serializers import RootFilmSerializer, RatingSerializer, FilmRatingSerializer

def db_table(request):
    return render(request, 'index.html')

class FilmFilter(FilterSet):
    class Meta:
        model = Film
        fields = dynamic_field_filters(model)

class RatingFilter(FilterSet):

    class Meta:
        model = Rating
        fields = dynamic_field_filters(model)

# These classes contain the bulk of the logic and are the most common place for customization
# Each class inherits from either a `ListCreateAPIView` class for general endpoints,
# and a `RetrieveUpdateDestroyAPIView` for specific id endpoints. These classes create functions
# for each of the http verbs (which can be easily customized, see `FilmRatingList`).
# The classes also control which serializer to use, and allow for the specification of filters,
# including an ordering filter. Pagination is applied to all rest requests, and is set in `settings.py`

class FilmList(generics.ListCreateAPIView):
    # The following query allows the fetching of all films, their related films details,
    # and the average rating all in one query.
    queryset = Film.objects.all().annotate(average_score=Avg('ratings__score'))
    serializer_class = RootFilmSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = FilmFilter

class FilmDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Film.objects.all().annotate(average_score=Avg('ratings__score'))
    serializer_class = RootFilmSerializer
    filter_class = FilmFilter

class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = RatingFilter

class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    filter_class = RatingFilter

class FilmRatingList(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = FilmRatingSerializer
    filter_class = RatingFilter

    def get_queryset(self):
        # Only return ratings for the specific film
        return Film.objects.get(**self.kwargs).ratings.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # save the serializer based on the film_id in the route
        serializer = FilmRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(film_id=kwargs['pk'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
