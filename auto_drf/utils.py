from django.apps import apps
from django.conf import settings

from django.db.models.fields.related import RelatedField
from django.db.models.fields.reverse_related import ForeignObjectRel

def get_auto_drf_models():
    return [apps.get_model(app_name, model_name)
            for app_name, models in settings.AUTO_DRF['MODELS'].items()
            for model_name in models]

def model_related_fields(model):
    return {field for field in model._meta.get_fields()
            if isinstance(field, (RelatedField, ForeignObjectRel))}

def all_table_fields(model):
    all_fields = [field.name for field in model._meta.fields]
    all_fields += [field.name for field in model_related_fields(model)]

    if hasattr(model, 'calculated_properties'):
        all_fields += list(model.calculated_properties().keys())

    return list(dict.fromkeys(all_fields))
