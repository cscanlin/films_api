from urllib.parse import urljoin

from django.conf import settings
from django.http import JsonResponse
from django_filters.filters import (
    BooleanFilter,
    CharFilter,
    NumberFilter,
)
from rest_framework.generics import ListCreateAPIView

from .auto_views import AUTO_VIEWS

API_ROOT_PATH = '/' + settings.AUTO_DRF.get('API_ROOT_PATH', 'api/')

FILTER_TYPE_LOOKUP = {
    BooleanFilter: 'boolean',
    CharFilter: 'string',
    NumberFilter: 'number',
}

def generate_auto_drf_schema(request):

    open_api_schema = {
        'openapi': '3.0.0',
        'info': {
            'version': '',
            'title': settings.AUTO_DRF.get('API_TITLE'),
            'description': '',
        },
        'servers': [{'url': API_ROOT_PATH}],
        'paths': {},
    }

    for view_name, view_class in AUTO_VIEWS.items():

        if not issubclass(view_class, ListCreateAPIView):
            continue

        view_relative_route = urljoin(API_ROOT_PATH, view_class.url_route)
        all_filters = view_class.filter_class.base_filters.copy()
        all_filters.update(view_class.filter_class.declared_filters)

        parameters = []
        for field_name, field_class in all_filters.items():
            parameters.append({
                'name': field_name,
                'in': 'query',
                'schema': {
                    'type': FILTER_TYPE_LOOKUP.get(field_class.__class__, 'string'),
                    'title': field_name,
                    'description': f'!!Filter',
                }
            })

        operation_id = view_class.serializer_class.Meta.model._meta.verbose_name_plural + '_list'
        open_api_schema['paths'][view_relative_route] = {
            'get': {
                'operationId': operation_id,
                'parameters': parameters,
            },
        }

    return JsonResponse(open_api_schema)
