from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel

RELATED_FIELD_TYPES = (RelatedField, ManyToOneRel, ManyToManyRel)

def dynamic_field_filters(model):
    return {field.name: field.__class__.class_lookups.keys()
            for field in model._meta.get_fields()
            if not isinstance(field, RELATED_FIELD_TYPES)}
