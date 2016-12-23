from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user_statistics.models import UserStatistics, UserScores, UserActor, UserDirector, UserGenre, UserNation
from user_statistics.serializations import StatisticsScoresSerializer, StatisticsActorSerializer, StatisticsDirectorSerializer, \
    StatisticsGenreSerializer, StatisticsNationSerializer


class StatisticsAll(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_statistics, created = UserStatistics.objects.get_or_create(user=user)
        user_scores, created = UserScores.objects.get_or_create(user_statistics=user_statistics)
        user_actors = UserActor.objects.filter(user_statistics=user_statistics).order_by('-count')[:10]
        user_directors = UserDirector.objects.filter(user_statistics=user_statistics).order_by('-count')[:10]
        user_genres = UserGenre.objects.filter(user_statistics=user_statistics).order_by('-count')[:7]
        user_nations = UserNation.objects.filter(user_statistics=user_statistics).order_by('-count')[:6]
        serial_scores = StatisticsScoresSerializer(user_scores)
        serial_actors = StatisticsActorSerializer(user_actors, many=True)
        serial_directors = StatisticsDirectorSerializer(user_directors, many=True)
        serial_genres = StatisticsGenreSerializer(user_genres, many=True)
        serial_nations = StatisticsNationSerializer(user_nations, many=True)
        return Response({'scores': serial_scores.data,
                         'actors': serial_actors.data,
                         'directors': serial_directors.data,
                         'genres': serial_genres.data,
                         'nations': serial_nations.data},
                        status=status.HTTP_200_OK)
