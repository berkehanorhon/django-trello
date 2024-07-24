from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated

from .models import CardAttachment, CardComment, CardTag, Card, List, Board, BoardMember, ListMember, CardMember
from .permissions import IsBoardAdmin
from .serializers import ListSerializer, CardSerializer, BoardSerializer, CardAttachmentSerializer, \
    CardCommentSerializer, CardTagSerializer


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return Board.objects.filter(members__user=self.request.user, members__is_active=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        BoardMember.objects.create(board=serializer.instance, user=self.request.user, is_active=True, is_admin=True)

    def perform_update(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsBoardAdmin]
        return super().get_permissions()


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return List.objects.filter(board__members__user=self.request.user, board__members__is_active=True)

    def perform_create(self, serializer):
        try:
            board = Board.objects.get(slug=self.request.data.get('board'))
        except ObjectDoesNotExist:
            raise NotFound("Board not found.")
        if not board.is_admin(self.request.user):
            raise PermissionDenied("You must be an admin to create a list.")
        serializer.save(created_by=self.request.user, board=board)
        ListMember.objects.create(list=serializer.instance, user=self.request.user, is_active=True)

    def perform_update(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsBoardAdmin]
        return super().get_permissions()


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return Card.objects.filter(list__board__members__user=self.request.user, list__board__members__is_active=True)

    def perform_create(self, serializer):
        try:
            list_instance = List.objects.get(slug=self.request.data.get('list'))
        except ObjectDoesNotExist:
            raise NotFound("List not found.")
        if not list_instance.board.is_admin(self.request.user):
            raise PermissionDenied("You must be an admin to create a card.")
        serializer.save(created_by=self.request.user, list=list_instance)
        CardMember.objects.create(card=serializer.instance, user=self.request.user, is_active=True)

    def perform_update(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsBoardAdmin]
        return super().get_permissions()


class CardAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = CardAttachmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return CardAttachment.objects.filter(card__list__board__members__user=self.request.user,
                                             card__list__board__members__is_active=True)

    def perform_create(self, serializer):
        try:
            card_instance = Card.objects.get(slug=self.request.data.get('card'))
        except ObjectDoesNotExist:
            raise NotFound("Card not found.")
        serializer.save(card=card_instance)

    def perform_update(self, serializer):
        serializer.save()


class CardCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CardCommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return CardComment.objects.filter(card__list__board__members__user=self.request.user,
                                          card__list__board__members__is_active=True)

    def perform_create(self, serializer):
        try:
            card_instance = Card.objects.get(slug=self.request.data.get('card'))
        except ObjectDoesNotExist:
            raise NotFound("Card not found.")
        serializer.save(card=card_instance, user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class CardTagViewSet(viewsets.ModelViewSet):
    serializer_class = CardTagSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return CardTag.objects.filter(card__list__board__members__user=self.request.user,
                                      card__list__board__members__is_active=True)

    def perform_create(self, serializer):
        try:
            card_instance = Card.objects.get(slug=self.request.data.get('card'))
        except ObjectDoesNotExist:
            raise NotFound("Card not found.")
        serializer.save(card=card_instance)

    def perform_update(self, serializer):
        serializer.save()
