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

        possible_moves = [{'x': position['x'] + 1, 'y': position['y']}, {'x': position['x'] - 1, 'y': position['y']},
                          {'x': position['x'], 'y': position['y'] + 1}, {'x': position['x'] + 1, 'y': position['y'] - 1}]

        for wall in walls_dict_list:
            walls.append((wall['x'], wall['y']))

        # Add ghosts next positions as walls
        for ghost in request.data['ghosts']:
            for possible_move in possible_moves:
                if possible_move['x'] == ghost['x'] and possible_move['y'] == ghost['y']:
                    walls.append((ghost['x'], ghost['y']))

                if possible_move['x'] == (ghost['x'] + 1) and possible_move['y'] == ghost['y']:
                    walls.append((ghost['x'] + 1, ghost['y']))

                if possible_move['x'] == (ghost['x'] - 1) and possible_move['y'] == ghost['y']:
                    walls.append((ghost['x'] - 1, ghost['y']))

                if possible_move['x'] == ghost['x'] and possible_move['y'] == (ghost['y'] + 1):
                    walls.append((ghost['x'], ghost['y'] + 1))

                if possible_move['x'] == ghost['x'] and possible_move['y'] == (ghost['y'] - 1):
                    walls.append((ghost['x'], ghost['y'] - 1))

        move = CalculateMove(width, height, walls, start, end)

        return Response({'move': move.nextMove()})
