from rest_framework import serializers
from .models import MyUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ["id", "email", "name", "password"]
        extra_kwargs = {
            'password': {'write_only': True},  # Exclude password field from serialized output
        }
    def create(self, validated_data):
        user = MyUser.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user
