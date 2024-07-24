from rest_framework import serializers

from .models import Board, List, Card


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['slug', 'name', 'description', 'is_active']
        read_only_fields = ['slug', 'created_by', 'created_at', 'updated_at']


class ListSerializer(serializers.ModelSerializer):
    board = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    board_name = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = ['slug', 'board', 'board_name', 'name', 'description', 'is_active']
        read_only_fields = ['slug', 'created_by', 'created_at', 'updated_at', 'board']

    def get_board_name(self, obj):
        return obj.board.name


class CardSerializer(serializers.ModelSerializer):
    list = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    list_name = serializers.SerializerMethodField()
    board_name = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ['slug', 'list', 'list_name', 'board_name', 'name', 'description', 'is_active']
        read_only_fields = ['slug', 'created_by', 'created_at', 'updated_at', 'list']

    def get_list_name(self, obj):
        return obj.list.name

    def get_board_name(self, obj):
        return obj.list.board.name
