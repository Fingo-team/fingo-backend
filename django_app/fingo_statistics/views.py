from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from fingo_statistics.models import UserActivity
from fingo_statistics.serializations import UserCommentsSerializer
from member.models import FingoUser
from member.serializations import UserSerializer


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.auth.user
        user_profile = FingoUser.objects.get(email=user.email)
        comment_cnt = UserActivity.objects.filter(user=user).exclude(comment=None).count()
        watched_movie_cnt = UserActivity.objects.filter(user=user).exclude(watched_movie=False).count()
        wish_movie_cnt = UserActivity.objects.filter(user=user).exclude(wish_movie=False).count()

        user_profile_serial = UserSerializer(user_profile)

        return Response({"user_profile": user_profile_serial.data,
                         "comment_cnt": comment_cnt,
                         "watched_movie_cnt": watched_movie_cnt,
                         "wish_movie_cnt": wish_movie_cnt},
                        status=status.HTTP_200_OK)


class UserComments(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.auth.user
        user_comments = UserActivity.objects.filter(user=user)#.order_by("-activity_time")

        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        paginator.ordering = "-activity_time"
        paged_comments = paginator.paginate_queryset(user_comments, request)

        serial = UserCommentsSerializer(paged_comments, many=True)

        return paginator.get_paginated_response(serial.data)


