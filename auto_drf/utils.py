from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
from django_filters.rest_framework.filterset import FILTER_FOR_DBFIELD_DEFAULTS

RELATED_FIELD_TYPES = (RelatedField, ManyToOneRel, ManyToManyRel)

def dynamic_field_filters(model):
    field_filters = {field.name: field.__class__.class_lookups.keys()
                     for field in model._meta.get_fields()
                     if not isinstance(field, RELATED_FIELD_TYPES)}
    return field_filters

def calculated_properties_filters(model):
    property_filters = {}
    if hasattr(model, 'calculated_properties'):
        for field_name, (field_type, _) in model.calculated_properties().items():
            for lookup_expr in field_type.class_lookups.keys():
                filter_type = FILTER_FOR_DBFIELD_DEFAULTS[field_type]['filter_class']
                filter_field = filter_type(field_name=field_name, lookup_expr=lookup_expr)
                property_filters[f'{field_name}__{lookup_expr}'] = filter_field
    return property_filters
