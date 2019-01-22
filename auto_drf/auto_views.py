from django_filters.rest_framework import FilterSet
from rest_framework import generics

from .auto_serializer import AUTO_SERIALIZERS
from .utils import dynamic_field_filters

# These classes contain the bulk of the logic and are the most common place for customization
# Each class inherits from either a `ListCreateAPIView` class for general endpoints,
# and a `RetrieveUpdateDestroyAPIView` for specific id endpoints. These classes create functions
# for each of the http verbs (which can be easily customized, see `FilmRatingList`).
# The classes also control which serializer to use, and allow for the specification of filters,
# including an ordering filter. Pagination is applied to all rest requests, and is set in `settings.py`

def generate_auto_views(auto_serializers):
    auto_views = {}
    for serializer_name, serializer_class in auto_serializers.items():
        model = serializer_class.Meta.model
        model_plural_name = str(model._meta.verbose_name_plural)

        filter_meta_attributes = {
            'model': model,
            'fields': dynamic_field_filters(model),
        }
        FilterMeta = type('Meta', (object, ), filter_meta_attributes)
        filter_class = type(serializer_name, (FilterSet,), {'Meta': FilterMeta})

        model_view_attributes = {
            'queryset': model.objects.all(),
            'serializer_class': serializer_class,
            'filter_class': filter_class,
        }

        list_view_name = model._meta.object_name + 'List'
        model_list_view = type(list_view_name,
                               (generics.ListCreateAPIView,),
                               model_view_attributes)
        model_list_view.url_route = '/'.join((model_plural_name, ''))
        auto_views[list_view_name] = model_list_view

        detail_view_name = model._meta.object_name + 'Detail'
        model_detail_view = type(detail_view_name,
                                 (generics.RetrieveUpdateDestroyAPIView,),
                                 model_view_attributes)
        model_detail_view.url_route = '/'.join((model_plural_name, '<int:pk>', ''))
        auto_views[detail_view_name] = model_detail_view

    return auto_views


AUTO_VIEWS = generate_auto_views(AUTO_SERIALIZERS)
