from rest_framework.response import Response
from rest_framework.views import APIView
from movie.models import Movie
from movie.serializations import MovieDetailSerializer


class MovieDetail(APIView):
    def get(self, request, *args, **kwargs):
        movie = Movie.objects.get(pk=kwargs.get("pk"))
        serial = MovieDetailSerializer(movie)

        return Response(serial.data)
