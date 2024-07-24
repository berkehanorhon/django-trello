from rest_framework import serializers

from .models import Board, List, Card, CardAttachment, CardComment, CardTag


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


class CardAttachmentSerializer(serializers.ModelSerializer):
    card = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    card_name = serializers.SerializerMethodField()

    class Meta:
        model = CardAttachment
        fields = ['slug', 'card', 'card_name', 'file', 'is_active']
        read_only_fields = ['slug', 'uploaded_at', 'card']

    def get_card_name(self, obj):
        return obj.card.name


class CardCommentSerializer(serializers.ModelSerializer):
    card = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    card_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = CardComment
        fields = ['slug', 'card', 'comment', 'is_active', 'commented_at', 'user_name', 'card_name']
        read_only_fields = ['slug', 'commented_at', 'card']

    def get_card_name(self, obj):
        return obj.card.name

    def get_user_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.sur_name

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CardTagSerializer(serializers.ModelSerializer):
    card = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    card_name = serializers.SerializerMethodField()

    class Meta:
        model = CardTag
        fields = ['slug', 'card', 'tag', 'is_active', 'card_name']
        read_only_fields = ['slug', 'card']

    def get_card_name(self, obj):
        return obj.card.name
