from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from movie.models import Movie, BoxofficeRank
from movie.serializations import MovieDetailSerializer, BoxofficeRankSerializer


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
