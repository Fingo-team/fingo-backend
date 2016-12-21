from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from utils.movie import searchMixin
from movie.serializations import SimpleMovieSerializer
from movie.models import Movie

__all__ = [
    "MovieSearch"
]


class MovieSearch(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SimpleMovieSerializer

    def get_queryset(self):
        movie_name = self.request.query_params.get('q')
        # DB에 충분한 data가 쌓일 시 아래 코드 활성화
        # movies = Movie.objects.filter(title__contains=movie_name)
        # if list(movies) == []:
        #     movies = searchMixin.search_movie(movie_name)
        searchMixin.search_movie(movie_name)
        fingodb_movies = Movie.objects.filter(title__contains=movie_name)

        self.paginator.ordering = "pk"

        return fingodb_movies
