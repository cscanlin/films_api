from django.apps import apps
from django.conf import settings
from django.db.models.fields.related import RelatedField, ManyToManyField
from django.db.models.fields.reverse_related import ForeignObjectRel, ManyToOneRel, ManyToManyRel
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

    base_serializers = {serializer_name + 'Base': type(
        serializer_name + 'Base',
        serializer_class.__bases__,
        dict(serializer_class.__dict__),
    ) for serializer_name, serializer_class in auto_serializers.items()}
    for serializer_name, serializer_class in auto_serializers.items():
        serializer_model = serializer_class.Meta.model
        relationship_fields = {field for field in serializer_model._meta.get_fields()
                               if isinstance(field, (RelatedField, ForeignObjectRel))}
        for field in relationship_fields:
            relationship_serializer_name = field.related_model._meta.object_name + 'Serializer'
            relationship_base_serializer = base_serializers.get(relationship_serializer_name + 'Base')
            nested_serializer = type(
                relationship_serializer_name + serializer_model.__name__ + 'Level_1',
                relationship_base_serializer.__bases__,
                dict(relationship_base_serializer.__dict__),
            )
            setattr(serializer_class, field.name,
                    nested_serializer(many=isinstance(field, (ManyToManyField, ManyToOneRel, ManyToManyRel)),
                                      required=False, read_only=True))
        serializer_class._declared_fields = serializer_class._get_declared_fields(
            serializer_class.__bases__,
            dict(serializer_class.__dict__),
        )
    return auto_serializers

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

    add_nested_serializers(auto_serializers)
    return auto_serializers


AUTO_SERIALIZERS = generate_auto_serializers()
