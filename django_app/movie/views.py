from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.pagination import CursorPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import Movie, BoxofficeRank
from fingo_statistics.models import UserActivity
from movie.serializations import MovieDetailSerializer, BoxofficeRankSerializer, BoxofficeMovieSerializer
from fingo_statistics.serializations import UserCommentSerializer
from movie import searchMixin


class MovieDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        # from IPython import embed; embed()
        serial = MovieDetailSerializer(movie, context={"request": request})

        return Response(serial.data)


class BoxofficeRankList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        ranking = BoxofficeRank.objects.all()
        ranking_serial = BoxofficeRankSerializer(ranking, many=True)
        ret = {
            "data": ranking_serial.data
        }
        return Response(ret)


class MovieSearch(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        movie_name = request.GET.get("q")
        # DB에 충분한 data가 쌓일 시 아래 코드 활성화
        # movies = Movie.objects.filter(title__contains=movie_name)
        # if list(movies) == []:
        #     movies = searchMixin.search_movie(movie_name)
        searchMixin.search_movie(movie_name)
        fingodb_movies = Movie.objects.filter(title__contains=movie_name)
        serial = BoxofficeMovieSerializer(fingodb_movies, many=True)
        return Response(serial.data)


class MovieScore(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.auth.user
        active = UserActivity.objects.get_or_create(user=user,
                                                    movie=movie)[0]
        user_score = float(request.POST["score"])
        try:
            if 0.0 <= user_score <= 5.0:
                active.score = user_score
                active.watched_movie = True
                active.wish_movie = False
                active.save()

                movie_scores = movie.useractivity_set.all().exclude(score=None)
                movie_average = sum([movie_score.score for movie_score in movie_scores]) / len(movie_scores)
                movie.score = movie_average
                movie.save()
                return Response(status=status.HTTP_200_OK)
            else:
                raise ValueError
        except ValueError:
            return Response({'error': 'score 값이 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class MovieComment(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        queryset = UserActivity.objects.filter(movie=movie)
        paginator = api_settings.DEFAULT_PAGINATION_CLASS()
        # OrderingFilter를 사용할 것 * 공식 문서 참고
        paginator.ordering = "-pk"
        paged_comments = paginator.paginate_queryset(queryset, request)
        serial = UserCommentSerializer(paged_comments, many=True,
                                       context={"request": request})

        return paginator.get_paginated_response(serial.data)

    def post(self, request, *args, **kwargs):
        user = request.auth.user
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        user_activity, created = UserActivity.objects.get_or_create(user=user,
                                                                    movie=movie)
        user_activity.comment = request.POST.get("comment")
        if created:
            user_activity.watched_movie = True
        user_activity.save()

        return Response({"info": "댓글이 등록되었습니다"}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        user = request.auth.user
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        try:
            user_activity = UserActivity.objects.get(user=user,
                                                     movie=movie)
        except UserActivity.DoesNotExist:
            return Response({"error": "수정할 댓글이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        user_activity.comment = request.POST.get("comment")
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
