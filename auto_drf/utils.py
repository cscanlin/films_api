from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel

RELATED_FIELD_TYPES = (RelatedField, ManyToOneRel, ManyToManyRel)

def dynamic_field_filters(model):
    field_filters = {field.name: field.__class__.class_lookups.keys()
                     for field in model._meta.get_fields()
                     if not isinstance(field, RELATED_FIELD_TYPES)}
    # if hasattr(model, 'calculated_properties'):
    #     property_filters = {field_name: field_type.class_lookups.keys()
    #                         for field_name, (field_type, _)
    #                         in model.calculated_properties().items()}
    #     field_filters.update(property_filters)
    return field_filters
