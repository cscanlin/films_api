from django.urls import path, re_path

from .views import AUTO_VIEWS
from .schema import generate_auto_drf_schema, SWAGGER_SCHEMA_VIEW

def generate_auto_urlpatterns(auto_views):
    auto_urlpatterns = []
    for view_name, view_class in auto_views.items():
        url_path = path(view_class.url_route, view_class.as_view())
        auto_urlpatterns.append(url_path)
    return auto_urlpatterns


urlpatterns = generate_auto_urlpatterns(AUTO_VIEWS)
urlpatterns += [
    path('open_api_schema.json', generate_auto_drf_schema),
    path('swagger/', SWAGGER_SCHEMA_VIEW.with_ui('swagger', cache_timeout=0)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', SWAGGER_SCHEMA_VIEW.without_ui(cache_timeout=0)),
]
