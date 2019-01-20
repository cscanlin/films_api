from rest_framework.metadata import SimpleMetadata

class FilterMetadata(SimpleMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        # serializer = view.filter_class.Meta.serializer_class
        filters = view.filter_class.Meta.fields
        model = view.filter_class.Meta.model

        # set field order with related fields last
        fields_w_relationships = [field.name for field in model._meta.get_fields()]
        db_fields = [field.name for field in model._meta.fields]
        db_fields += [rel_field for rel_field in fields_w_relationships
                      if rel_field not in db_fields]
        metadata['ordered_fields'] = db_fields

        metadata['fields'] = dict(list(metadata['actions'].values()).pop())

        if hasattr(model, 'relations_diplay_fields'):
            for field_name, display_accessor in model.relations_diplay_fields().items():
                metadata['fields'][field_name]['display_accessor'] = display_accessor

        for field_name, field_filters in filters.items():
            metadata['fields'][field_name]['filters'] = field_filters
        metadata.pop('actions', {})

        return metadata
