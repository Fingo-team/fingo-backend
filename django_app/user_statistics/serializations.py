from rest_framework import serializers
from user_statistics.models import UserStatistics, UserScores, UserActor
from movie.serializations import ActorSerializer


class StatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatistics
        fields = '__all__'


class StatisticsScoresSerializer(serializers.ModelSerializer):
    user_statistics = StatisticsSerializer(read_only=True)

    class Meta:
        model = UserScores
        fields = '__all__'


class StatisticsActorsSerializer(serializers.ModelSerializer):
    user_statistics = StatisticsSerializer(read_only=True)
    actor = ActorSerializer(read_only=True)

    class Meta:
        model = UserActor
        fields = '__all__'
