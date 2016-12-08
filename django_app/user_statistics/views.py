from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from fingo_statistics.models import UserActivity
from user_statistics.models import UserStatistics, UserScores
from user_statistics.serializations import ScoresSerializer


class StatisticsScores(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        user_statistics, created = UserStatistics.objects.get_or_create(user=user)
        user_scores, created = UserScores.objects.get_or_create(user_statistics=user_statistics)
        serial = ScoresSerializer(user_scores)
        return Response(serial.data, status=status.HTTP_200_OK)
