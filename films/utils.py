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
