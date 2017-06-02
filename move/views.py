from rest_framework.views import APIView
from rest_framework.response import Response
from move.models import Wall, Game
from move.serializers import WallSerializer, GameSerializer
from move.move import CalculateMove


class Move(APIView):
    def post(self, request, format=None):
        stored_game = Game.objects.all().last()

        # Clean maze if we start a new game
        if stored_game.gameId != request.data['player']['id']:
            Wall.objects.all().delete()
            game_serializer = GameSerializer(stored_game, data={'gameId': request.data['player']['id']}, partial=True)

            if game_serializer.is_valid():
                game_serializer.save()

        # Add new parts of the maze discovered
        walls = WallSerializer.remove_duplicates(request.data['maze']['walls'])
        serializer = WallSerializer(data=walls, many=True)

        if serializer.is_valid():
            serializer.save()

        # Get maze information and calculate next move
        stored_walls = Wall.objects.all()
        serializer = WallSerializer(stored_walls, many=True)
        walls_dict_list = serializer.data

        height = request.data['maze']['size']['height']
        width = request.data['maze']['size']['width']
        position = request.data['player']['position']
        start = (position['x'], position['y'])
        goal = request.data['maze']['goal']
        end = (goal['x'], goal['y'])
        walls = []

        for wall in walls_dict_list:
            walls.append((wall['x'], wall['y']))

        move = CalculateMove(width, height, walls, start, end)

        return Response({'move': move.nextMove()})
