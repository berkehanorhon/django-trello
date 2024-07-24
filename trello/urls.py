from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BoardViewSet, ListViewSet, CardViewSet

router = DefaultRouter()
router.register(r'boards', BoardViewSet, "board")
router.register(r'lists', ListViewSet, "list")
router.register(r'cards', CardViewSet, "card")

urlpatterns = [
    path('', include(router.urls)),
]
