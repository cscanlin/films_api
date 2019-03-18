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
from rest_framework.serializers import ListSerializer

from .auto_views import AUTO_VIEWS
from .utils import all_table_fields

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
        schema = get_schema(view_class)
        open_api_schema['components']['schemas'][schema_name] = schema

        view_relative_route = urljoin(API_ROOT_PATH, view_class.url_route)
        open_api_schema['paths'][view_relative_route] = get_path(view_class, schema)

    return JsonResponse(open_api_schema)

def get_schema(view_class):
    properties = {}
    model = view_class.serializer_class.Meta.model
    for field_name, field_obj in view_class.serializer_class().get_fields().items():
        properties[field_name] = {
            'type': FIELD_TYPE_LOOKUP.get(field_obj.__class__, 'string'),
            'x-childFields': isinstance(field_obj, ListSerializer),
        }
        if hasattr(model, 'relations_diplay_fields'):
            display_accessor = model.relations_diplay_fields().get(field_name)
            properties[field_name]['x-displayAccessor'] = display_accessor

    return {
        'type': 'object',
        'properties': properties,
        'x-fieldOrder': all_table_fields(view_class.serializer_class.Meta.model),
    }

def get_path(view_class, schema):

    all_filters = view_class.filter_class.base_filters.copy()
    all_filters.update(view_class.filter_class.declared_filters)

    parameters = []
    for filter_name, filter_obj in all_filters.items():
        parameters.append({
            'name': filter_name,
            'in': 'query',
            'schema': {
                'type': FILTER_TYPE_LOOKUP.get(filter_obj.__class__, 'string'),
                'title': filter_name,
                'description': '',
            },
            'x-filterParam': True,
            'x-relatedField': filter_name.split('__')[0],
        })
    operation_id = view_class.serializer_class.Meta.model._meta.verbose_name_plural + '_list'
    return {
        'get': {
            'operationId': operation_id,
            'parameters': parameters,
            'responses': {
                '200': {
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'array',
                                'items': schema,
                            },
                        },
                    },
                },
            },
        },
    }
