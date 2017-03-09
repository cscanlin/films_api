from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Film, Rating

class FilmTests(APITestCase):

    def test_create_film(self):
        client = APIClient()
        response = client.post('/films/', {'title': 'created film'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.count(), 1)
        self.assertEqual(Film.objects.get().title, 'created film')

    def test_retrieve_film(self):
        client = APIClient()
        film = Film.objects.create(title='retrieved film')
        response = client.get('/films/{}/'.format(film.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.get().title, 'retrieved film')

    def test_list_films(self):
        client = APIClient()
        film0 = Film.objects.create(title='listed film 1')
        film1 = Film.objects.create(title='listed film 2')
        response = client.get('/films/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['title'], film0.title)
        self.assertEqual(response.data['results'][1]['title'], film1.title)

    def test_film_average_score(self):
        film = Film.objects.create(title='ranked film')
        Rating.objects.create(film=film, score=4)
        Rating.objects.create(film=film, score=6)
        self.assertEqual(film.average_score, 5)

class RatingTests(APITestCase):
    def test_add_rating_general(self):
        client = APIClient()
        api_route = '/ratings/'
        film = Film.objects.create(title='ranked film')
        response = client.post(api_route, {'film': film.id, 'score': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)

    def test_add_rating_film(self):
        client = APIClient()
        film = Film.objects.create(title='ranked film')
        api_route = 'film/{}/ratings/'.format(film.id)
        response = client.post(api_route, {'score': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Film.objects.get().ratings.count(), 1)
