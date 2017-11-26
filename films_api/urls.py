"""films_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import api_controller

# Defines the routes and connects matching view/controller functionality.
# Supports top level routes for `/films` and `/ratings`,
# as well as support for nested routes like `/films/<id>/ratings`

urlpatterns = [
    url(r'^api/v1/films/?$', api_controller.FilmList.as_view()),
    url(r'^api/v1/films/(?P<pk>[0-9]+)/?$', api_controller.FilmDetail.as_view()),
    url(r'^api/v1/films/(?P<pk>[0-9]+)/ratings/?$', api_controller.FilmRatingList.as_view()),
    url(r'^api/v1/films/(?P<film_id>[-\w]+)/ratings/(?P<pk>[0-9]+)/?$', api_controller.RatingDetail.as_view()),
    url(r'^api/v1/ratings/?$', api_controller.RatingList.as_view()),
    url(r'^api/v1/ratings/(?P<pk>[0-9]+)/?$', api_controller.RatingDetail.as_view()),
    url(r'^admin/?', admin.site.urls),
    url(r'^docs/?', include('rest_framework_docs.urls')),
    url(r'^$', api_controller.home, name='home'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
