from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
import rest_framework_filters as filters

from .utils import get_auto_drf_models, model_related_fields

RELATED_FIELD_TYPES = (RelatedField, ManyToOneRel, ManyToManyRel)

def dynamic_field_filters(model):
    field_filters = {field.name: list(field.__class__.class_lookups.keys())
                     for field in model._meta.get_fields()
                     if not isinstance(field, RELATED_FIELD_TYPES)}
    return field_filters

def calculated_properties_filters(model):
    property_filters = {}
    if hasattr(model, 'calculated_properties'):
        for field_name, (field_type, _) in model.calculated_properties().items():
            for lookup_expr in field_type.class_lookups.keys():
                filter_type = filters.FilterSet.FILTER_DEFAULTS[field_type]['filter_class']
                filter_field = filter_type(field_name=field_name, lookup_expr=lookup_expr)
                property_filters[f'{field_name}__{lookup_expr}'] = filter_field
    return property_filters

def related_filters(model):
    related_filters = {}
    for rel_field in model_related_fields(model):
        related_filters[rel_field.name] = filters.RelatedFilter(
            '.'.join((__name__, rel_field.related_model.__name__ + 'Filter')),
            field_name=rel_field.name,
            queryset=rel_field.related_model.objects.all(),
        )
    return related_filters

def generate_auto_filters():
    auto_filters = {}

    for model in get_auto_drf_models():
        filter_meta_attributes = {
            'model': model,
            'fields': dynamic_field_filters(model),
        }
        FilterMeta = type('Meta', (object, ), filter_meta_attributes)
        filter_attributes = {
            'Meta': FilterMeta,
            **related_filters(model),
            **calculated_properties_filters(model),
        }
        filter_class_name = model.__name__ + 'Filter'
        filter_class = type(
            filter_class_name,
            (filters.FilterSet,),
            filter_attributes,
        )
        auto_filters[filter_class_name] = filter_class

    return auto_filters


AUTO_FILTERS = generate_auto_filters()

def __getattr__(name):
    if name in AUTO_FILTERS:
        return AUTO_FILTERS.get(name)
    raise AttributeError(f'module {__name__} has no attribute {name}')
