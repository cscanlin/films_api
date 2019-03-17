from django.urls import path

from .auto_schema import generate_auto_drf_schema_view
from .auto_views import AUTO_VIEWS

def generate_auto_urlpatterns(auto_views):
    auto_urlpatterns = []
    for view_name, view_class in auto_views.items():
        url_path = path(view_class.url_route, view_class.as_view())
        auto_urlpatterns.append(url_path)
    return auto_urlpatterns


urlpatterns = generate_auto_urlpatterns(AUTO_VIEWS)
urlpatterns.append(path('schema/', generate_auto_drf_schema_view))
