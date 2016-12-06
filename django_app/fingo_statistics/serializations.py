from rest_framework import serializers
from fingo_statistics.models import UserActivity
from member.serializations import UserSerializer


class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = serializers.ReadOnlyField(source="movie.title")

    class Meta:
        model = UserActivity
        fields = ("user",
                  "movie",
                  "comment",
                  "score",)


class UserCommentSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserActivity
        fields = ("user",
                  "comment",)
