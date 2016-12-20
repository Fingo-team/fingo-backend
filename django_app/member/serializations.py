from rest_framework import serializers
from member.models import FingoUser


class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingoUser
        fields = ("email",
                  "password",)


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingoUser
        fields = ("email",
                  "nickname",
                  "password",)

    def create(self, validated_data):
        user = FingoUser.objects.create_user(**validated_data)

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingoUser
        fields = ("id",
                  "nickname",
                  "level",
                  "user_img_url",
                  "cover_img_url",)
