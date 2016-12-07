from rest_framework import serializers
from member.models import FingoUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingoUser
        fields = ("id",
                  "nickname",
                  "level",
                  "user_img",
                  "cover_img",)