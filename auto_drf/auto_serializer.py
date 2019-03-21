from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
from rest_framework import serializers

from .utils import get_auto_drf_models, model_related_fields, all_table_fields

MANY_REL_TYPES = (ManyToManyField, ManyToOneRel, ManyToManyRel)

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    # Looks for `fields` in the query_params and removes any not listed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            fields_string = self.context['request'].query_params['fields']
        except (KeyError, AttributeError):
            return
        for field_name in set(self.fields.keys()) - set(fields_string.split(',')):
            self.fields.pop(field_name)

def add_nested_serializers(auto_serializers):

    base_serializers = {serializer_name: type(
        serializer_name,
        serializer_class.__bases__,
        dict(serializer_class.__dict__),
    ) for serializer_name, serializer_class in auto_serializers.items()}

    for serializer_name, serializer_class in auto_serializers.items():
        serializer_model = serializer_class.Meta.model

        for rel_field in model_related_fields(serializer_model):
            relationship_serializer_name = rel_field.related_model._meta.object_name + 'Serializer'
            nested_serializer = type(
                relationship_serializer_name + serializer_model.__name__ + 'Level_1',
                base_serializers[relationship_serializer_name].__bases__,
                dict(base_serializers[relationship_serializer_name].__dict__),
            )

            nested_serializer_instance = nested_serializer(
                many=isinstance(rel_field, MANY_REL_TYPES),
                required=False,
                read_only=True,
            )
            setattr(serializer_class, rel_field.name, nested_serializer_instance)

        serializer_declared_fields = serializer_class._get_declared_fields(
            serializer_class.__bases__,
            dict(serializer_class.__dict__),
        )
        serializer_class._declared_fields.update(serializer_declared_fields)
    return auto_serializers

def generate_auto_serializers():

    auto_serializers = {}
    for model in get_auto_drf_models():

        swagger_schema_fields = {
            'x-orderedFields': all_table_fields(model)
        }
        if hasattr(model, 'relations_diplay_fields'):
            swagger_schema_fields['x-relationsDiplayFields'] = model.relations_diplay_fields()

        meta_attributes = {
            'model': model,
            'fields': '__all__',
            'swagger_schema_fields': swagger_schema_fields,
        }

        Meta = type('Meta', (object,), meta_attributes)

        additional_attrs = {}
        if hasattr(model, 'calculated_properties'):
            for k, v in model.calculated_properties().items():
                serializer_field_type = getattr(serializers, v[0].__name__)
                additional_attrs[k] = serializer_field_type(read_only=True, required=False)

        serializer_name = model._meta.object_name + 'Serializer'
        serializer_class = type(serializer_name,
                                (DynamicFieldsModelSerializer,),
                                {'Meta': Meta, **additional_attrs})
        auto_serializers[serializer_name] = serializer_class

    add_nested_serializers(auto_serializers)

    return auto_serializers


AUTO_SERIALIZERS = generate_auto_serializers()

def __getattr__(name):
    if name in AUTO_SERIALIZERS:
        return AUTO_SERIALIZERS.get(name)
    raise AttributeError(f'module {__name__} has no attribute {name}')
