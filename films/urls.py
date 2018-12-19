from django.urls import path
from . import api_controller

# Defines the routes and connects matching view/controller functionality.
# Supports top level routes for `/films` and `/ratings`,
# as well as support for nested routes like `/films/<id>/ratings`

urlpatterns = [
    path('films/', api_controller.FilmList.as_view()),
    path('films/<int:pk>/', api_controller.FilmDetail.as_view()),
    path('films/<slug:url_slug>/', api_controller.FilmDetail.as_view(lookup_field='url_slug')),
    path('films/<int:pk>/ratings/', api_controller.FilmRatingList.as_view()),
    path('films/<str:url_slug>/ratings/', api_controller.FilmRatingList.as_view(lookup_field='url_slug')),
    path('films/<str:film_id>/ratings/<int:pk>', api_controller.RatingDetail.as_view()),
    path('ratings/', api_controller.RatingList.as_view()),
    path('ratings/<int:pk>/', api_controller.RatingDetail.as_view()),
    # path('admin/', admin.site.urls),
    # path('docs/', include('rest_framework_docs.urls')),  # django_rest_framework_redocs
    path('', api_controller.home, name='home'),
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
