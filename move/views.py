from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from move.models import Wall
from move.serializers import WallSerializer
from django.http import HttpResponse
from move.astar import AStar

class Move(APIView):
    def post(self, request, format=None):
        walls = WallSerializer.remove_duplicates(request.data['maze']['walls'])
        serializer = WallSerializer(data=walls, many=True)

        if serializer.is_valid():
            serializer.save()
            # stored_walls = Wall.objects.all()
            # serializer = WallSerializer(stored_walls, many=True)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)

        stored_walls = Wall.objects.all()
        serializer = WallSerializer(stored_walls, many=True)
        wallsDictList = serializer.data

        height = request.data['maze']['size']['height']
        width = request.data['maze']['size']['width']
        position = request.data['player']['position']
        start = (position['x'], position['y'])
        goal = request.data['maze']['goal']
        end = (goal['x'], goal['y'])

        walls = []
        for wall in wallsDictList:
            walls.append((wall['x'], wall['y']))

        aStar = AStar()
        aStar.init_grid(width, height, walls, start, end)
        path = aStar.solve()

        return HttpResponse(str(path))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
