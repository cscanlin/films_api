from django.db import models

FIELD_FILTERS_MAP = {
    models.CharField: ['icontains'],
    models.IntegerField: ['lte', 'gte'],
}

def dynamic_field_filters(model):
    fields = {}
    for field in model._meta.get_fields():
        if field.__class__ in FIELD_FILTERS_MAP.keys():
            fields[field.name] = FIELD_FILTERS_MAP[field.__class__]
    return fields

def all_table_fields(model):
    fields_w_relationships = [field.name for field in model._meta.get_fields()]
    all_table_fields = [field.name for field in model._meta.fields]
    all_table_fields += [rel_field for rel_field in fields_w_relationships
                         if rel_field not in all_table_fields]

    # support for auto_drf
    if hasattr(model, 'calculated_properites'):
        all_table_fields += list(model.calculated_properites().keys())

    return all_table_fields
