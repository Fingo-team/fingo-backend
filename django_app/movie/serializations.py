from rest_framework import serializers
from movie.models import Movie, Actor, Director, StillCut, BoxofficeRank


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ("name",
                  "img",)


class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = ("name",
                  "img",)


class StillcutSerializer(serializers.ModelSerializer):

    class Meta:
        model = StillCut
        fields = ("img",)


class MovieDetailSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True, many=True)
    director = DirectorSerializer(read_only=True, many=True)
    stillcut = StillcutSerializer(read_only=True,
                                  many=True,
                                  source="stillcut_set")

    class Meta:
        model = Movie
        fields = ("title",
                  "actor",
                  "director",
                  "genre",
                  "story",
                  "img",
                  "stillcut",
                  "first_run_date",
                  "score",
                  "nation_code",)


class BoxOfficeRankSerializer(serializers.ModelSerializer):
    movie = MovieDetailSerializer()

    class Meta:
        model = BoxofficeRank
        fields = ("rank",
                  "movie",)
