from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from movie.models import Movie
from movie.serializations import MovieDetailSerializer
from fingo_statistics.models import UserActivity
from fingo_statistics.serializations import MovieCommentsSerializer


__all__ = [
    "MovieDetail",
    "MovieComments"
]


class MovieDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.all()


class MovieComments(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MovieCommentsSerializer

    def get_queryset(self):
        movie = self.kwargs.get("pk")
        queryset = UserActivity.objects.filter(movie=movie) \
            .exclude(comment=None).order_by("-activity_time")

        self.paginator.ordering = "-activity_time"

        return queryset
