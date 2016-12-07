from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from fingo_statistics.models import UserActivity
from movie.models import Movie, BoxofficeRank
from movie.serializations import MovieDetailSerializer, BoxofficeRankSerializer, BoxofficeMovieSerializer
from movie import searchMixin

from utils.statistics import average


class MovieDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        serial = MovieDetailSerializer(movie)

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

                average.score_average(movie)
                return Response(status=status.HTTP_200_OK)
            else:
                raise ValueError
        except ValueError:
            return Response({'error': 'score 값이 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


class MovieWish(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.auth.user
        active = UserActivity.objects.get_or_create(user=user,
                                                    movie=movie)[0]
        return Response({'wish_movie': active.wish_movie}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.auth.user
        active = UserActivity.objects.get_or_create(user=user,
                                                    movie=movie)[0]
        if request.POST["wish_movie"] == "True":
            wish_movie = True
        elif request.POST["wish_movie"] == "False":
            wish_movie = False
        else:
            return Response({'error': '올바른 형식이 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)
        active.wish_movie = wish_movie
        active.watched_movie = not wish_movie

        if wish_movie:
            active.score = None
            active.save()
            average.score_average(movie)
        else:
            active.save()

        return Response({'info': '해당 영화의 보고싶어요를 {} 처리 했습니다.'.format(wish_movie)}, status=status.HTTP_200_OK)
