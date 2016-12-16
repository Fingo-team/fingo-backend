from rest_framework import serializers
from fingo_statistics.models import UserActivity
from member.serializations import UserSerializer
from movie.serializations import UserPageMovieSerializer, UserActivityMoviesDetailSerializer
from django.utils.dateparse import parse_datetime


class TimeConvertModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        parsing_time = parse_datetime(ret["activity_time"]).replace(microsecond=0)
        ret["activity_time"] = parsing_time.strftime("%Y-%m-%d %H:%M:%S")

        return ret


class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    movie = serializers.ReadOnlyField(source="movie.title")

    class Meta:
        model = UserActivity
        fields = ("user",
                  "movie",
                  "comment",
                  "score",)


class MovieCommentsSerializer(TimeConvertModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserActivity
        fields = ("user",
                  "movie",
                  "comment",
                  "score",
                  "activity_time",)


class UserCommentsSerializer(TimeConvertModelSerializer):
    user = UserSerializer()
    movie = UserPageMovieSerializer()

    class Meta:
        model = UserActivity
        fields = ("user",
                  "comment",
                  "score",
                  "activity_time",
                  "movie")


class UserActivityMoviesSerializer(TimeConvertModelSerializer):
    movie = UserActivityMoviesDetailSerializer()

    class Meta:
        model = UserActivity
        fields = ("activity_time",
                  "movie")


class UserCommentCreateSerailizer(serializers.ModelSerializer):

    class Meta:
        model = UserActivity
        fields = ("comment",
                  "movie",)

    def create(self, validated_data):
        ua = UserActivity(**validated_data)
        user = self.context.get("request").auth.user
        ua.user = user
        ua.movie = validated_data.get("movie")
        ua.watched_movie = True
        ua.save()

        return ua

    def update(self, instance, validated_data):
        instance.comment = validated_data.get("comment")
        instance.save()

        return instance
