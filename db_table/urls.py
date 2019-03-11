from django.urls import re_path
from . import views

# Defines the routes and connects matching view/controller functionality.
# Supports top level routes for `/films` and `/ratings`,
# as well as support for nested routes like `/films/<id>/ratings`

urlpatterns = [
    re_path(r'.*', views.db_table, name='db_table'),
]
