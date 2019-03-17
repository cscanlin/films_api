from django.conf import settings

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONOpenAPIRenderer
from rest_framework.schemas import SchemaGenerator
from rest_framework.response import Response

class AutoDRFSchemaGenerator(SchemaGenerator):

    def get_links(self, request):
        links = super().get_links(request)
        for document_name, node in links.items():
            for method, link in node.links:
                if str(method) != 'list':
                    continue
                for field in link.fields:
                    if '__' in field.name:
                        field.description = '!!Filter' + (field.description or '')
                    print(field)
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
