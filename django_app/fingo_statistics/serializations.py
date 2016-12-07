from rest_framework import serializers
from fingo_statistics.models import UserActivity
from member.serializations import UserSerializer
from movie.serializations import UserPageMovieSerializer


class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = serializers.ReadOnlyField(source="movie.title")

    class Meta:
        model = UserActivity
        fields = ("user",
                  "movie",
                  "comment",
                  "score",)


class MovieCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserActivity
        fields = ("user",
                  "comment",
                  "score",)


class UserCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = UserPageMovieSerializer()

    class Meta:
        model = UserActivity
        fields = ("user",
                  "comment",
                  "score",
                  "activity_time",
                  "movie")