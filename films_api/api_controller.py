from django.http import JsonResponse


from .models import Test

def test_func(request):
    return JsonResponse({'foo': Test.objects.get(pk=1).name})
