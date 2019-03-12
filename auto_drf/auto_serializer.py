from django.apps import apps
from django.conf import settings
from django.db.models.fields.related import RelatedField, ManyToManyField
from django.db.models.fields.reverse_related import ForeignObjectRel
from rest_framework import serializers

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

def add_nested_serializers(auto_serializers):
    nesting_level = settings.AUTO_DRF.get('SERIALIZE_NESTED_LEVEL', 0)
    if nesting_level == 0:
        return auto_serializers

    nested_serializers = {}
    for serializer_name, serializer_class in auto_serializers.items():
        serializer_model = serializer_class.Meta.model
        relationship_fields = {field for field in serializer_model._meta.get_fields()
                               if isinstance(field, (RelatedField, ForeignObjectRel))}
        for field in relationship_fields:
            relationship_serializer_name = field.model._meta.object_name + 'Serializer'
            relationship_root_serializer = auto_serializers.get(relationship_serializer_name)
            nested_serializer = type(
                relationship_serializer_name + 'Level_1',
                relationship_root_serializer.__bases__,
                dict(relationship_root_serializer.__dict__),
            )
            setattr(relationship_root_serializer, field.name,
                    nested_serializer(many=isinstance(field, ManyToManyField)))
            nested_serializers[nested_serializer.__name__] = nested_serializer
            nested_serializers[relationship_serializer_name] = relationship_root_serializer
    return nested_serializers

def generate_auto_serializers():
    # load auto_models from AUTO_DRF['MODELS']
    auto_models = {'.'.join((app_name, 'models', model_name)): apps.get_model(app_name, model_name)
                   for app_name, models in settings.AUTO_DRF['MODELS'].items()
                   for model_name in models}

    auto_serializers = {}
    for model_name, model in auto_models.items():
        meta_attributes = {
            'model': model,
            'fields': all_table_fields(model),
        }
        Meta = type('Meta', (object,), meta_attributes)

        serializer_name = model._meta.object_name + 'Serializer'
        serializer_class = type(serializer_name,
                                (DynamicFieldsModelSerializer,),
                                {'Meta': Meta})
        auto_serializers[serializer_name] = serializer_class

    auto_serializers.update(add_nested_serializers(auto_serializers))
    return auto_serializers


AUTO_SERIALIZERS = generate_auto_serializers()
