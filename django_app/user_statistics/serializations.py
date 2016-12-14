from rest_framework import serializers
from user_statistics.models import UserStatistics, UserScores, UserActor, UserDirector, UserGenre, UserNation
from movie.serializations import ActorSerializer , DirectorSerializer, GenreSerializer, NationSerializer


class StatisticsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatistics
        fields = '__all__'


class StatisticsScoresSerializer(serializers.ModelSerializer):
    user_statistics = StatisticsSerializer(read_only=True)

    class Meta:
        model = UserScores
        fields = '__all__'


class StatisticsActorSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)

    class Meta:
        model = UserActor
        fields = ('actor', 'count',)


class StatisticsDirectorSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(read_only=True)

    class Meta:
        model = UserDirector
        fields = ('director', 'count',)


class StatisticsGenreSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = UserGenre
        fields = ('genre', 'count',)


class StatisticsNationSerializer(serializers.ModelSerializer):
    nation = NationSerializer(read_only=True)

    class Meta:
        model = UserNation
        fields = ('nation', 'count',)
