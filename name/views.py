from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from name.models import Name
from name.serializers import NameSerializer

@csrf_exempt
def name_details(request):
    """
    List user details
    """
    if request.method == 'GET':
        name = Name.objects.all()
        serializer = NameSerializer(name, many=True)
        return JsonResponse(serializer.data, safe=False)
