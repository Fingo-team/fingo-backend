from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework import status
from fingo_statistics.models import UserActivity
from member.serializations import UserSerializer
from movie.serializations import UserPageMovieSerializer, ActivityAsMovieSerializer
from django.utils.dateparse import parse_datetime


class CommentDoesNotExisit(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = u"댓글을 입력해 주세요"


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
    movie = ActivityAsMovieSerializer()

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
        if validated_data["comment"] is None:
            raise CommentDoesNotExisit()
        instance.comment = validated_data["comment"]
        instance.save()

        return instance
