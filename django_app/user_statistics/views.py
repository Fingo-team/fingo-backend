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
        user = request.auth.user

        user_statistics, created = UserStatistics.objects.get_or_create(user=user)
        user_scores, created = UserScores.objects.get_or_create(user_statistics=user_statistics)

        user_activities = UserActivity.objects.filter(user=user).filter(watched_movie=True)
        user_statistics.count(user_activities)
        self.set_scores(user_activities, user_scores)
        serial = ScoresSerializer(user_scores)
        return Response(serial.data, status=status.HTTP_200_OK)

    def set_scores(self, user_activities, user_scores):
        user_scores.reset()
        for user_activity in user_activities:
            user_scores.set_score(user_activity)
