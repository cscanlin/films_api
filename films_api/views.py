import os

from django.http import HttpResponse
from django.conf import settings

def index(request):
    try:
        with open(os.path.join(settings.BASE_DIR, 'build', 'index.html')) as f:
            return HttpResponse(f.read())
    except FileNotFoundError:
        error_msg = (
            'This URL is only used when you have built the production '
            'version of the app. Visit http://localhost:3000/ instead, or '
            'run `npm run build` to test the production version.'
        )
        return HttpResponse(error_msg, status=501)
