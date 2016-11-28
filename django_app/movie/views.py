from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from movie.models import Movie, BoxofficeRank
from movie.serializations import MovieDetailSerializer, BoxOfficeRankSerializer


class MovieDetail(APIView):
    def get(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        serial = MovieDetailSerializer(movie)

        return Response(serial.data)


class BoxOfficeRankList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        ranking = BoxofficeRank.objects.all()
        ranking_serial = {
            "data":
            [
                BoxOfficeRankSerializer(rank).data
                for rank
                in ranking
            ]
        }
        return Response(ranking_serial)
