from rest_framework import serializers
from member.models import FingoUser


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingoUser
        fields = ("email",
                  "nickname",
                  "password",)

    def create(self, validated_data):
        user = FingoUser(**validated_data)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingoUser
        fields = ("id",
                  "nickname",
                  "level",
                  "user_img",
                  "cover_img",)