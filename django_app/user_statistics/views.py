from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user_statistics.models import UserStatistics, UserScores, UserActor, UserDirector, UserGenre, UserNation
from user_statistics.serializations import StatisticsScoresSerializer, StatisticsActorSerializer, StatisticsDirectorSerializer, \
    StatisticsGenreSerializer, StatisticsNationSerializer


class StatisticsScores(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_statistics, created = UserStatistics.objects.get_or_create(user=user)
        user_scores, created = UserScores.objects.get_or_create(user_statistics=user_statistics)
        serial = StatisticsScoresSerializer(user_scores)
        return Response(serial.data, status=status.HTTP_200_OK)


class StatisticsActors(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_statistics, created = UserStatistics.objects.get_or_create(user=user)
        user_actors = UserActor.objects.filter(user_statistics=user_statistics).order_by('-count')
        serial = StatisticsActorSerializer(user_actors, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)


class StatisticsDirectors(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_statistics, created = UserStatistics.objects.get_or_create(user=user)
        user_directors = UserDirector.objects.filter(user_statistics=user_statistics).order_by('-count')
        serial = StatisticsDirectorSerializer(user_directors, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)


class StatisticsGenres(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_statistics, created = UserStatistics.objects.get_or_create(user=user)
        user_genres = UserGenre.objects.filter(user_statistics=user_statistics).order_by('-count')
        serial = StatisticsGenreSerializer(user_genres, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)


class StatisticsNations(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_statistics, created = UserStatistics.objects.get_or_create(user=user)
        user_nations = UserNation.objects.filter(user_statistics=user_statistics).order_by('-count')
        serial = StatisticsNationSerializer(user_nations, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
