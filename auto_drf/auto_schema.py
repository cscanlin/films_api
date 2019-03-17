from django.conf import settings

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import OpenAPIRenderer, JSONOpenAPIRenderer
from rest_framework.schemas import SchemaGenerator
from rest_framework.response import Response


class AutoDRFSchemaGenerator(SchemaGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_links(self, request):
        links = super().get_links(request)
        print(vars(links['films']))
        return links


@api_view()
@renderer_classes([JSONOpenAPIRenderer])
def generate_auto_drf_schema_view(request):
    generator = AutoDRFSchemaGenerator(
        title=settings.AUTO_DRF.get('API_TITLE'),
        url='/' + settings.AUTO_DRF.get('API_ROOT_PATH', 'api/'),
        urlconf='auto_drf.auto_urls',
    )
    return Response(generator.get_schema())
