from rest_framework.metadata import SimpleMetadata

from .utils import all_table_fields

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
        metadata['ordered_fields'] = all_table_fields(model)

        metadata['fields'] = dict(list(metadata['actions'].values()).pop())

        if hasattr(model, 'relations_diplay_fields'):
            for field_name, display_accessor in model.relations_diplay_fields().items():
                metadata['fields'][field_name]['display_accessor'] = display_accessor

        for field_name, field_filters in filters.items():
            metadata['fields'][field_name]['filters'] = field_filters
        metadata.pop('actions', {})

        return metadata
