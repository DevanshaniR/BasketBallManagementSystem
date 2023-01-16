from rest_framework import serializers

from .models import Game, Team, Player, UserLoginDetails


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        many = True
        model = Game
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        many = True
        model = Player
        fields = ['id', 'name', 'height', 'team']
