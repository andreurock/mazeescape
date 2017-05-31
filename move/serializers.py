from rest_framework import serializers
from move.models import Wall

class WallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wall
        fields = ('x', 'y')

    def remove_duplicates(walls):
        stored_walls = Wall.objects.all()
        serializer = WallSerializer(stored_walls, many=True)

        for stored_wall in serializer.data:
            i = 0
            for new_wall in walls:
                if stored_wall['x'] == new_wall['x'] and stored_wall['y'] == new_wall['y']:
                    walls.pop(i)
                    break
                i += 1

        return walls