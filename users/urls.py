from django.urls import path

from .views import RegisterView, LoginView, TestAuthentication, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('check_token', TestAuthentication.as_view(), name='check_token'),
    path('logout', LogoutView.as_view(), name='logout'),
]
