from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from move.models import Wall, Game
from move.serializers import WallSerializer, GameSerializer
from django.http import HttpResponse
from move.move import CalculateMove

class Move(APIView):
    def post(self, request, format=None):
        walls = WallSerializer.remove_duplicates(request.data['maze']['walls'])
        serializer = WallSerializer(data=walls, many=True)

        stored_game = Game.objects.all().last()

        return HttpResponse(str(stored_game.gameId))


        if stored_game != request.data['player']['id']:
            Wall.objects.all().delete()
            gameSerializer = GameSerializer(stored_game, data=request.data['player']['id'])
            if gameSerializer.is_valid():
                gameSerializer.save()

        if serializer.is_valid():
            serializer.save()

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

        move = CalculateMove(width, height, walls, start, end)

        stored_walls = Wall.objects.all()
        serializer = WallSerializer(stored_walls, many=True)

        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)

        return HttpResponse(str(serializer.data))

        return Response({'move' : move.nextMove()})
