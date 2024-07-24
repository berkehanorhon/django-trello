from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='check_token'),
    path('token/check', TokenVerifyView.as_view(), name='check_token'),
    path('logout', LogoutView.as_view(), name='logout'),
]
