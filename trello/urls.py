from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BoardViewSet, ListViewSet, CardViewSet, CardAttachmentViewSet, CardCommentViewSet, CardTagViewSet

router = DefaultRouter()
router.register(r'boards', BoardViewSet, "board")
router.register(r'lists', ListViewSet, "list")
router.register(r'cards', CardViewSet, "card")
router.register(r'attachments', CardAttachmentViewSet, "attachment")
router.register(r'comments', CardCommentViewSet, "comment")
router.register(r'tags', CardTagViewSet, "tag")
urlpatterns = [
    path('', include(router.urls)),
]
