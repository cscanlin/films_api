from rest_framework.metadata import SimpleMetadata

class FilterMetadata(SimpleMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        filters = view.filter_class.Meta.fields
        for field_name, field_filters in filters.items():
            metadata['actions']['POST'][field_name]['filters'] = field_filters
        return metadata
