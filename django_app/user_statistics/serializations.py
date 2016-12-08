from rest_framework import serializers
from user_statistics.models import UserStatistics, UserScores


class StatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatistics
        fields = '__all__'


class ScoresSerializer(serializers.ModelSerializer):
    user_statistics = StatisticsSerializer(read_only=True)

    class Meta:
        model = UserScores
        fields = '__all__'
