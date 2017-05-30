from rest_framework import serializers
from name.models import Name

class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ('name', 'email')