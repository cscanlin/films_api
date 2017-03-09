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

    def test_create_film_with_related(self):
        client = APIClient()
        related_film = Film.objects.create(title='related film')
        response = client.post(
            '/films/', {'title': 'created film', 'related_films': [related_film.id]}, format='json'
        )

        self.assertEqual(response.data['related_films'][0], related_film.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        self.assertEqual(film._average_score, 5)

class RatingTests(APITestCase):

    def setUp(self):
        self.film = Film.objects.create(title='ranked film')

    def test_create_rating(self):
        client = APIClient()
        api_route = '/ratings/'
        response = client.post(api_route, {'film': self.film.id, 'score': 5}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)

    def test_retrieve_rating(self):
        client = APIClient()
        rating = Rating.objects.create(film=self.film, score=4)
        response = client.get('/ratings/{}/'.format(rating.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rating = Rating.objects.get()
        self.assertEqual(rating.film.id, self.film.id)
        self.assertEqual(rating.score, 4)

    def test_list_ratings(self):
        client = APIClient()
        Rating.objects.create(film=self.film, score=4)
        Rating.objects.create(film=self.film, score=6)
        response = client.get('/ratings/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        results = response.data['results']
        self.assertEqual(results[0]['film'], self.film.id)
        self.assertEqual(results[0]['score'], 4)
        self.assertEqual(results[1]['film'], self.film.id)
        self.assertEqual(results[1]['score'], 6)

    def test_list_film_ratings(self):
        client = APIClient()
        Rating.objects.create(film=self.film, score=4)
        Rating.objects.create(film=self.film, score=6)
        api_route = '/films/{}/ratings/'.format(self.film.id)
        response = client.get(api_route, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Film.objects.get().ratings.count(), 2)
        results = response.data['results']
        self.assertEqual(results[0]['score'], 4)
        self.assertEqual(results[1]['score'], 6)
