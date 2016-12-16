from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.db.utils import IntegrityError

from movie.models import Movie, BoxofficeRank
from fingo_statistics.models import UserActivity
from movie.serializations import BoxofficeRankDetailSerializer
from movie.serializations import MovieDetailSerializer, BoxofficeRankSerializer, BoxofficeMovieSerializer
from fingo_statistics.serializations import MovieCommentsSerializer, UserCommentCreateSerailizer, UserCommentsSerializer
from movie import searchMixin

from utils.statistics import average, count_all


class MovieDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all()

    # def get(self, request, *args, **kwargs):
    #     movie = Movie.objects.get(pk=kwargs.get("pk"))
    #     serial = MovieDetailSerializer(movie, context={"request": request})
    #
    #     return Response(serial.data)


class BoxofficeRankList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoxofficeRankSerializer
    queryset = BoxofficeRank.objects.all().order_by("rank")
    pagination_class = None

    # def get_queryset(self):
    #     queryset = self.queryset
    #     return queryset.order_by("rank")


class BoxofficeRankDetailList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        ranking = BoxofficeRank.objects.all()
        ranking_serial = BoxofficeRankDetailSerializer(ranking, many=True)
        ret = {
            "data": ranking_serial.data
        }
        return Response(ret)


class MovieSearch(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        movie_name = request.query_params.get('q')
        # DB에 충분한 data가 쌓일 시 아래 코드 활성화
        # movies = Movie.objects.filter(title__contains=movie_name)
        # if list(movies) == []:
        #     movies = searchMixin.search_movie(movie_name)
        searchMixin.search_movie(movie_name)
        fingodb_movies = Movie.objects.filter(title__contains=movie_name)
        serial = BoxofficeMovieSerializer(fingodb_movies, many=True)
        return Response(serial.data)


class MovieWish(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        active = UserActivity.objects.get_or_create(user=user,
                                                    movie=movie)[0]
        return Response({'wish_movie': active.wish_movie}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        active = UserActivity.objects.get_or_create(user=user,
                                                    movie=movie)[0]
        if request.data.get("wish_movie") == "True":
            wish_movie = True
        elif request.data.get("wish_movie") == "False":
            wish_movie = False
        else:
            return Response({'error': '올바른 형식이 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        change_average = False

        if not active.wish_movie and active.watched_movie and wish_movie:
            count_all(movie, active.score, -1, user)
            active.score = float(0)
            change_average = True
            active.watched_movie = False

        active.wish_movie = wish_movie
        active.save()

        if change_average:
            average.score_average(movie)

        return Response({'wish_movie': active.wish_movie}, status=status.HTTP_200_OK)


class MovieComments(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MovieCommentsSerializer
    queryset = UserActivity.objects.all()

    def list(self, request, *args, **kwargs):
        movie = kwargs.get("pk")
        queryset = self.get_queryset().filter(movie=movie)
        self.paginator.ordering = "-activity_time"
        page = self.paginate_queryset(queryset)
        serial_data = self.get_serializer(page, many=True)

        return self.get_paginated_response(serial_data.data)


    # def get(self, request, *args, **kwargs):
    #     try:
    #         movie = Movie.objects.get(pk=kwargs.get("pk"))
    #     except Movie.DoesNotExist:
    #         return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     queryset = UserActivity.objects.filter(movie=movie)
    #     paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    #     # OrderingFilter를 사용할 것 *공식 문서 참고
    #     paginator.ordering = "-activity_time"
    #     paged_comments = paginator.paginate_queryset(queryset, request)
    #     serial = MovieCommentsSerializer(paged_comments, many=True)
    #
    #     return paginator.get_paginated_response(serial.data)


class MovieAsUserComment(generics.RetrieveUpdateDestroyAPIView,
                         generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCommentCreateSerailizer
    queryset = UserActivity.objects.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = request.auth.user
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        ua = get_object_or_404(queryset, user=user, movie=movie)
        serial_data = UserCommentsSerializer(ua)

        return Response(serial_data.data)

    # def post(self, request, *args, **kwargs):
    #     # movie = Movie.objects.get(pk=kwargs.get("pk"))
    #     serializer = self.get_serializer_class()
    #     serial_data = serializer(data=request.data,
    #                              context={"request": request})
    #     if serial_data.is_valid():
    #         serial_data.save()
    #
    #     return Response({"info": "댓글이 등록되었습니다"}, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        request.data["movie"] = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            return Response({"error": "이미 있는 comment입니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def patch(self, request, *args, **kwargs):
        user = request.auth.user
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        ua = UserActivity.objects.get(user=user, movie=movie)
        serial = self.get_serializer(ua,
                                     data=request.data,
                                     partial=True)

        if serial.is_valid():
            self.perform_update(serial)
        try:
            user_activity = UserActivity.objects.get(user=user,
                                                     movie=movie)
        except UserActivity.DoesNotExist:
            return Response({"error": "수정할 댓글이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        user_activity.comment = request.data.get("comment")
        user_activity.save()

        return Response({"info": "댓글이 수정되었습니다."}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = request.auth.user
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        user_activity = UserActivity.objects.get(user=user,
                                                 movie=movie)

        if user_activity.score is None and user_activity.wish_movie is False:
            user_activity.delete()
        elif user_activity.score is not None:
            user_activity.comment = None
            user_activity.save()

        return Response({"info": "댓글이 삭제되었습니다."}, status=status.HTTP_200_OK)


class MovieScore(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.auth.user
        active = UserActivity.objects.get_or_create(user=user,
                                                    movie=movie)[0]
        return Response({'score': active.score}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.auth.user
        active = UserActivity.objects.get_or_create(user=user,
                                                    movie=movie)[0]
        user_score = float(request.data.get("score"))
        if 0.5 <= user_score <= 5.0:
            active.score = user_score
            count_all(movie, active.score, +1, user)
            active.watched_movie = True
            active.wish_movie = False
            active.save()
            average.score_average(movie)
            return Response({'info': '점수가 올바르게 들어갔습니다.'}, status=status.HTTP_200_OK)
        elif user_score == 0.0:
            count_all(movie, active.score, -1, user)
            active.score = 0.0
            active.watched_movie = False
            active.save()
            average.score_average(movie)
            return Response({'info': '해당 영화의 평가가 리셋됩니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'score 값이 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class MovieRandomList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        uas = UserActivity.objects.filter(user=user)
        movie_ids = [ua.movie.id for ua in uas]
        random_movies = Movie.objects.order_by("?").exclude(id__in=movie_ids)[:30]
        serial = BoxofficeMovieSerializer(random_movies, many=True)
        ret = {
            'data': serial.data
        }
        return Response(ret, status=status.HTTP_200_OK)
