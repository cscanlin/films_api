from django.http import JsonResponse


from .models import Film

def get_film(request, film_id):
    film = Film.objects.get(pk=film_id)
    return JsonResponse(film.serialize())
