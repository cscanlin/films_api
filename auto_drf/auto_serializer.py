from rest_framework import serializers

from django.apps import apps
from django.conf import settings
# from django.db.models import fields

from .utils import all_table_fields

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    # Looks for `fields` in the query_params and removes any not listed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            fields_string = self.context['request'].query_params['fields']
        except KeyError:
            return
        for field_name in set(self.fields.keys()) - set(fields_string.split(',')):
            self.fields.pop(field_name)

def generate_auto_serializers():
    # load auto_models from AUTO_DRF['MODELS']
    auto_models = {'.'.join((app_name, 'models', model_name)): apps.get_model(app_name, model_name)
                   for app_name, models in settings.AUTO_DRF['MODELS'].items()
                   for model_name in models}

    # auto_models[0]._meta.verbose_name_plural
    auto_serializers = {}
    from pprint import pprint
    for model_name, model in auto_models.items():
        # print(model_name)
        # pprint(vars(model))
        pprint(model._meta.get_fields())
        meta_attributes = {
            'model': model,
            'fields': all_table_fields(model),
        }
        Meta = type('Meta', (object, ), meta_attributes)

        for model_field in model._meta.local_fields:
            if model_field.remote_field:
                pass
                # print(model_field.model)
                # print(vars(vars(model_field)['remote_field']))
            # print(vars(model_field)['remote_field'])

        serializer_name = model._meta.object_name + 'Serializer'
        serializer_attributes = {
            'Meta': Meta,
        }
        serializer_class = type(serializer_name,
                                (DynamicFieldsModelSerializer, ),
                                serializer_attributes)
        auto_serializers[serializer_name] = serializer_class

    for serializer_name, serializer_class in auto_serializers.items():
        pass

    return auto_serializers


AUTO_SERIALIZERS = generate_auto_serializers()
