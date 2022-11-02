from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from users.models import Seller, BookStoreUser


class BookStoreUserRegisterSerializer(RegisterSerializer):
    is_seller = serializers.BooleanField()  # Don't validate is_seller because it is boolean.

    def custom_signup(self, request, user):
        user.is_seller = self.data['is_seller']
        if user.is_seller:
            Seller.objects.create(user=user)
        user.save()



