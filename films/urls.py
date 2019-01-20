from django.urls import path
from . import views

# Defines the routes and connects matching view/controller functionality.
# Supports top level routes for `/films` and `/ratings`,
# as well as support for nested routes like `/films/<id>/ratings`

urlpatterns = [
    path('films/', views.FilmList.as_view()),
    path('films/<int:pk>/', views.FilmDetail.as_view()),
    path('films/<slug:url_slug>/', views.FilmDetail.as_view(lookup_field='url_slug')),
    path('films/<int:pk>/ratings/', views.FilmRatingList.as_view()),
    path('films/<str:url_slug>/ratings/', views.FilmRatingList.as_view(lookup_field='url_slug')),
    path('films/<str:film_id>/ratings/<int:pk>', views.RatingDetail.as_view()),
    path('ratings/', views.RatingList.as_view()),
    path('ratings/<int:pk>/', views.RatingDetail.as_view()),
    # path('docs/', include('rest_framework_docs.urls')),  # django_rest_framework_redocs
    path('', views.home, name='home'),
]
