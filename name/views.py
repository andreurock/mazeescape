from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from name.models import Name
from name.serializers import NameSerializer

class GetPlayerInfo(APIView):
    """
    List user details
    """
    def post(self, request, format=None):
        name = Name.objects.all()
        serializer = NameSerializer(name, many=True)
        return Response(serializer.data[0])
