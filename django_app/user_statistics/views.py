from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from user_statistics.models import UserStatistics, UserScores, UserActor
from user_statistics.serializations import StatisticsScoresSerializer, StatisticsActorsSerializer


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
        serial = StatisticsActorsSerializer(user_actors, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
