from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from fingo_statistics.models import UserActivity
from fingo_statistics.serializations import UserCommentsSerializer, UserActivityMoviesSerializer
from member.models import FingoUser
from member.serializations import UserSerializer
from utils.movie.ordering_mixin import OrderingSelect


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        ua = UserActivity.objects.filter(user=self.request.auth.user)
        return ua

    def retrieve(self, request, *args, **kwargs):
        user = request.auth.user
        user_profile = FingoUser.objects.get(email=user.email)
        comment_cnt = self.get_queryset(user=user).exclude(comment=None).count()
        watched_movie_cnt = self.get_queryset(user=user).exclude(watched_movie=False).count()
        wish_movie_cnt = self.get_queryset(user=user).exclude(wish_movie=False).count()

        user_profile_serial = self.get_serializer(user_profile)

        return Response({"user_profile": user_profile_serial.data,
                         "comment_cnt": comment_cnt,
                         "watched_movie_cnt": watched_movie_cnt,
                         "wish_movie_cnt": wish_movie_cnt},
                        status=status.HTTP_200_OK)


class UserCommentsSelect(generics.ListAPIView, OrderingSelect):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCommentsSerializer

    def get_queryset(self):
        ordering_request = self.request.query_params.get("order")
        ordering = self.get_ordering_param(ordering_request)
        user_comments = UserActivity.objects.filter(user=self.request.auth.user).\
            exclude(comment=None).order_by(ordering)

        self.paginator.ordering = ordering

        return user_comments


class UserWishMoviesSelect(generics.ListAPIView, OrderingSelect):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserActivityMoviesSerializer

    def get_queryset(self):
        user = self.request.auth.user
        ordering_request = self.request.query_params.get("order")
        ordering = self.get_ordering_param(ordering_request)
        user_wish_movies = UserActivity.objects.filter(user=user). \
            filter(wish_movie=True).order_by(ordering)
        self.paginator.ordering = ordering
        self.paginator.page_size = 30

        return user_wish_movies

    # def get(self, request, *args, **kwargs):
    #     user = request.auth.user
    #     ordering_request = request.query_params.get("order")
    #     ordering = self.get_ordering_param(ordering_request)
    #     user_wish_movies = UserActivity.objects.filter(user=user).\
    #         filter(wish_movie=True).order_by(ordering)
    #
    #     paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    #     paginator.ordering = ordering
    #     paginator.page_size = 30
    #     paged_wish_movies = paginator.paginate_queryset(user_wish_movies, request)
    #
    #     serial = UserActivityMoviesSerializer(paged_wish_movies, many=True)
    #
    #     return paginator.get_paginated_response(serial.data)


class UserWatchedMoviesSelect(generics.ListAPIView, OrderingSelect):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserActivityMoviesSerializer

    def get_queryset(self):
        user = self.request.auth.user
        ordering_request = self.request.query_params.get("order")
        ordering = self.get_ordering_param(ordering_request)
        user_wish_movies = UserActivity.objects.filter(user=user). \
            filter(wish_movie=True).order_by(ordering)
        self.paginator.ordering = ordering
        self.paginator.page_size = 30

        return user_wish_movies

    # def get(self, request, *args, **kwargs):
    #     user = request.auth.user
    #     ordering_request = request.query_params.get("order")
    #     ordering = self.get_ordering_param(ordering_request)
    #     user_watched_movies = UserActivity.objects.filter(user=user).\
    #         filter(watched_movie=True).order_by(ordering)
    #
    #     paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    #     paginator.ordering = ordering
    #     paginator.page_size = 30
    #     paged_watched_movies = paginator.paginate_queryset(user_watched_movies, request)
    #
    #     serial = UserActivityMoviesSerializer(paged_watched_movies, many=True)
    #
    #     return paginator.get_paginated_response(serial.data)

