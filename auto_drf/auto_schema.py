from urllib.parse import urljoin

from django.conf import settings
from django.http import JsonResponse
from django_filters.filters import (
    BooleanFilter,
    CharFilter,
    NumberFilter,
)
from rest_framework.fields import (
    CharField,
    FloatField,
    IntegerField,
)
from rest_framework.generics import ListCreateAPIView

from .auto_views import AUTO_VIEWS

API_ROOT_PATH = '/' + settings.AUTO_DRF.get('API_ROOT_PATH', 'api/')

FILTER_TYPE_LOOKUP = {
    BooleanFilter: 'boolean',
    CharFilter: 'string',
    NumberFilter: 'number',
}

FIELD_TYPE_LOOKUP = {
    CharField: 'string',
    FloatField: 'number',
    IntegerField: 'integer',
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
        'components': {'schemas': {}}
    }
    for view_class in AUTO_VIEWS.values():
        if not issubclass(view_class, ListCreateAPIView):
            continue

        schema_name = view_class.serializer_class.Meta.model.__name__
        open_api_schema['components']['schemas'][schema_name] = get_schema(view_class)
        schema_path = '#/components/schemas/' + schema_name

        view_relative_route = urljoin(API_ROOT_PATH, view_class.url_route)
        open_api_schema['paths'][view_relative_route] = get_path(view_class, schema_path)

    return JsonResponse(open_api_schema)

def get_schema(view_class):
    properties = {}
    for field_name, field_type in view_class.serializer_class().get_fields().items():
        properties[field_name] = {
            'type': FIELD_TYPE_LOOKUP.get(field_type.__class__, 'string')
        }

    return {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': properties,
        },
    }
    """
    components:
      schemas:
        User:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
    """

def get_path(view_class, schema_path):

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
                'description': '!!Filter',
            }
        })

    operation_id = view_class.serializer_class.Meta.model._meta.verbose_name_plural + '_list'
    list_schema = {
        'type': 'array',
        'items': {
            '$ref': schema_path,
        },
    }
    return {
        'get': {
            'operationId': operation_id,
            'parameters': parameters,
            'responses': {
                '200': {'content': {'application/json': {'schema': list_schema}}}
            },
        },
    }
