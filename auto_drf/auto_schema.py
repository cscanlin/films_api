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
from rest_framework.serializers import ListSerializer, ModelSerializer
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view

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

def get_schema(view_class):
    properties = {}
    model = view_class.serializer_class.Meta.model
    for field_name, field_obj in view_class.serializer_class().get_fields().items():

        if isinstance(field_obj, ListSerializer):
            field_type = 'array'
        elif isinstance(field_obj, ModelSerializer):
            field_type = 'object'
        else:
            field_type = FIELD_TYPE_LOOKUP.get(field_obj.__class__, 'string')
        properties[field_name] = {'type': field_type}

    schema = {
        'type': 'object',
        'properties': properties,
        'x-orderedFields': all_table_fields(view_class.serializer_class.Meta.model),
    }
    if hasattr(model, 'relations_diplay_fields'):
        schema['x-relationsDiplayFields'] = model.relations_diplay_fields()

    return schema

def get_path(view_class, schema):

    all_filters = view_class.filter_class.base_filters.copy()
    all_filters.update(view_class.filter_class.declared_filters)
    # print(vars(view_class.filter_class))
    # print('')

    parameters = []
    for filter_name, filter_obj in all_filters.items():

        try:
            related_field, lookup_expr = filter_name.split('__')
        except ValueError:
            related_field, lookup_expr = filter_name, 'exact'

        parameters.append({
            'name': filter_name,
            'in': 'query',
            'schema': {
                'type': FILTER_TYPE_LOOKUP.get(filter_obj.__class__, 'string'),
                'title': filter_name,
            },
            'x-relatedField': related_field,
            'x-filterDescription': lookup_expr,
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


class AutoDRFSchemaGenerator(OpenAPISchemaGenerator):

    def get_operation(self, view, path, prefix, method, components, request):
        operation = super().get_operation(view, path, prefix, method, components, request)
        for parameter in operation['parameters']:
            try:
                related_field, lookup_expr = parameter['name'].split('__')
            except ValueError:
                related_field, lookup_expr = parameter['name'], 'exact'
            setattr(parameter, 'x-relatedField', related_field)
            setattr(parameter, 'x-filterDescription', lookup_expr)
        return operation


SWAGGER_SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title=settings.AUTO_DRF.get('API_TITLE'),
        default_version='v1',
        description='',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
    generator_class=AutoDRFSchemaGenerator
)
