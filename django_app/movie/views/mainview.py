from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from movie.serializations import SimpleMovieSerializer, BoxofficeRankSerializer,\
    BoxofficeRankDetailSerializer
from movie.models import Movie, BoxofficeRank, Genre
from fingo_statistics.models import UserActivity


__all__ = [
    "MovieMainView",
    "BoxofficeRankList",
    "BoxofficeRankDetailList",
    "MonthMovieList",
    "GenreMovieList",
    "MovieRandomList"
]

# Main Page
class MovieMainView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        this_month = datetime.now().month
        boxoffice = BoxofficeRank.objects.first().movie
        boxoffice_stillcut = boxoffice.stillcut_set.first().img
        boxoffice_url = "http://"+request.META["HTTP_HOST"]+reverse("api:movie:boxoffice")
        month_movie_queryset = Movie.objects.filter(first_run_date__month=this_month)[:1]
        month_movie_stillcut = month_movie_queryset[0].stillcut_set.first().img
        month_movie_url = "http://"+request.META["HTTP_HOST"]+reverse("api:movie:month")
        random_genre = Genre.objects.all().order_by("?")[:1]
        genre_name = random_genre[0].name
        genre_movie_queryset = Movie.objects.filter(genre__name=genre_name)
        genre_movie_stillcut = genre_movie_queryset[0].stillcut_set.first().img
        genre_movie_url = "http://"+request.META["HTTP_HOST"] \
                          +reverse("api:movie:genre")+ \
                          "?genre={genre}".format(genre=genre_name)

        ret_dic = {
            "boxoffice_stillcut": boxoffice_stillcut,
            "boxoffice_url": boxoffice_url,
            "month": this_month,
            "month_movie_stillcut": month_movie_stillcut,
            "month_movie_url": month_movie_url,
            "genre": genre_name,
            "genre_movie_stillcut": genre_movie_stillcut,
            "genre_movie_url": genre_movie_url
        }

        return Response({"data": ret_dic}, status=status.HTTP_200_OK)


# Boxoffice
class BoxofficeRankList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoxofficeRankSerializer
    queryset = BoxofficeRank.objects.all().order_by("rank")
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serial = self.get_serializer(queryset, many=True)

        return Response({"data": serial.data}, status=status.HTTP_200_OK)


class BoxofficeRankDetailList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoxofficeRankDetailSerializer
    queryset = BoxofficeRank.objects.all()
    pagination_class = None

    def list(self, request, *args, **kwargs):
        ranking = self.get_queryset()
        ranking_serial = self.get_serializer(ranking, many=True)
        return Response({"data": ranking_serial.data}, status=status.HTTP_200_OK)


# movie category
class MonthMovieList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleMovieSerializer
    pagination_class = None

    def get_queryset(self):
        this_month = datetime.now().month
        queryset = Movie.objects.filter(first_run_date__month=this_month) \
                       .order_by("score")[:10]

        return queryset

    def list(self, request, *args, **kwargs):
        serial = self.get_serializer(self.get_queryset(), many=True)
        return Response({"data": serial.data}, status=status.HTTP_200_OK)


class GenreMovieList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleMovieSerializer
    pagination_class = None

    def get_queryset(self):
        genre = self.request.query_params.get("genre")
        queryset = Movie.objects.filter(genre__name=genre) \
                       .order_by("score")[:10]

        return queryset

    def list(self, request, *args, **kwargs):
        serial = self.get_serializer(self.get_queryset(), many=True)
        return Response({"data": serial.data}, status=status.HTTP_200_OK)


# random movie
class MovieRandomList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleMovieSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        uas = UserActivity.objects.filter(user=user)
        movie_ids = [ua.movie.id for ua in uas]
        random_movies = Movie.objects.order_by("?").exclude(id__in=movie_ids, img=None)[:30]

        return random_movies

    def list(self, request, *args, **kwargs):
        serial = self.get_serializer(self.get_queryset(), many=True)
        return Response({"data": serial.data}, status=status.HTTP_200_OK)
