from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from fingo_statistics.models import UserActivity
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
                         "wish_movie_cnt": wish_movie_cnt})

