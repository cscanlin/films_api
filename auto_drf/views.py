from rest_framework import generics
from rest_framework.serializers import ListSerializer

from .filters import AUTO_FILTERS
from .serializer import AUTO_SERIALIZERS

def get_queryset(model, nested_field_name):
    return lambda self: getattr(model.objects.get(**self.kwargs), nested_field_name).all()

def generate_auto_views(auto_serializers):
    auto_views = {}
    for serializer_name, serializer_class in auto_serializers.items():
        model = serializer_class.Meta.model
        model_plural_name = str(model._meta.verbose_name_plural)

        if hasattr(model, 'get_queryset'):
            queryset = model.get_queryset()
        else:
            queryset = model.objects.all()

        if hasattr(model, 'calculated_properties'):
            property_annotations = {k: v[1] for k, v in model.calculated_properties().items()}
            queryset = queryset.annotate(**property_annotations)

        for nested_field_name, nested_serializer in serializer_class._declared_fields.items():
            if isinstance(nested_serializer, ListSerializer):
                nested_serializer_obj = nested_serializer._kwargs['child']
                related_model = nested_serializer_obj.__class__.Meta.model
                nested_list_view_name = model._meta.object_name + related_model.__name__ + 'List'
                model_view_attributes = {
                    'serializer_class': nested_serializer_obj.__class__,
                    'filter_class': AUTO_FILTERS.get(related_model.__name__ + 'Filter'),
                    'get_queryset': get_queryset(model, nested_field_name),
                    'url_route': '/'.join((model_plural_name, '<int:pk>', nested_field_name, ''))
                }
                nested_model_list_view = type(nested_list_view_name,
                                              (generics.ListCreateAPIView,),
                                              model_view_attributes)
                auto_views[nested_list_view_name] = nested_model_list_view

        model_view_attributes = {
            'queryset': queryset,
            'serializer_class': serializer_class,
            'filter_class': AUTO_FILTERS.get(model.__name__ + 'Filter'),
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

def __getattr__(name):
    if name in AUTO_VIEWS:
        return AUTO_VIEWS.get(name)
    raise AttributeError(f'module {__name__} has no attribute {name}')
