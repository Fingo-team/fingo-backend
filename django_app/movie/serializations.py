from rest_framework import serializers
from movie.models import Movie, Actor, Director, StillCut, BoxofficeRank, Genre, Nation, MovieActorDetail


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ("name",
                  "img",)


class ActorDetailSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)

    class Meta:
        model = MovieActorDetail
        fields = ("actor",
                  "role",)


class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = ("name",
                  "img",)


class StillcutSerializer(serializers.ModelSerializer):

    class Meta:
        model = StillCut
        fields = ("img",)


class NationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nation
        fields = ("name",)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("name",)


class MovieTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ("title",)


class MovieDetailSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(read_only=True, many=True)
    genre = GenreSerializer(read_only=True, many=True)
    nation_code = NationSerializer(read_only=True, many=True)
    actors = ActorDetailSerializer(read_only=True,
                                   many=True,
                                   source="movieactordetail_set")
    stillcut = StillcutSerializer(read_only=True,
                                  many=True,
                                  source="stillcut_set")

    class Meta:
        model = Movie
        fields = ("title",
                  "actors",
                  "director",
                  "genre",
                  "story",
                  "img",
                  "stillcut",
                  "first_run_date",
                  "score",
                  "nation_code",)


class BoxofficeMovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    nation_code = NationSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ("id",
                  "title",
                  "genre",
                  "img",
                  "first_run_date",
                  "score",
                  "nation_code",)


class BoxofficeRankSerializer(serializers.ModelSerializer):
    movie = BoxofficeMovieSerializer()

    class Meta:
        model = BoxofficeRank
        fields = ("rank",
                  "movie",)


class UserPageMovieSerializer(serializers.ModelSerializer):
    stillcut = StillcutSerializer(read_only=True,
                                  many=True,
                                  source="stillcut_set")

    class Meta:
        model = Movie
        fields = ("id",
                  "title",
                  "img",
                  "stillcut")


class UserActivityMoviesDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ("id",
                  "title",
                  "img",
                  "score",
                  "first_run_date")


class BoxofficeRankDetailSerializer(serializers.ModelSerializer):
    movie = MovieDetailSerializer()

    class Meta:
        model = BoxofficeRank
        fields = ("rank",
                  "movie",)
