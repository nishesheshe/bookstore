from django.urls import path
from .views import (
    BookStoreUserRegisterView,
    BookStoreUserCurrentView,
    BookStoreUserViewSet,
    BookCreateView,
)
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
)
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', BookStoreUserViewSet, basename='user')
urlpatterns = [
    path('signup', BookStoreUserRegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('me', BookStoreUserCurrentView.as_view()),
    path('create_book', BookCreateView.as_view()),
] + router.urls