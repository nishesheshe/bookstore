from django.urls import path
from .views import (
    BookStoreUserRegisterView
)
urlpatterns = [
    path('', BookStoreUserRegisterView.as_view()),
]