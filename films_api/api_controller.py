from django.http import JsonResponse

from .models import Film
from .serializers import RootFilmSerializer

def get_film(request, film_id):
    film = Film.objects.get(pk=film_id)
    serializer = RootFilmSerializer(film)
    return JsonResponse(serializer.data)
