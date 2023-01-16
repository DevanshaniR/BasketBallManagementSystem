from rest_framework import serializers

from .models import Game, Team, Player, UserLoginDetails


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        many = True
        model = Game
        fields = '__all__'








