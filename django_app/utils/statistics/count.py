from django.db import transaction

from user_statistics.models import UserActor, UserDirector, UserGenre, UserNation, UserStatistics, UserScores

__all__ = [
    'count_all',
]


def count_actor(movie, value, user):
    actors = movie.actor.all()
    for actor in actors:
        user_actor, created = UserActor.objects.get_or_create(actor=actor,
                                                              user_statistics=user.userstatistics)
        user_actor.count += value
        if user_actor.count:
            user_actor.save()
        else:
            user_actor.delete()


def count_director(movie, value, user):
    directors = movie.director.all()
    for director in directors:
        user_director, created = UserDirector.objects.get_or_create(director=director,
                                                                    user_statistics=user.userstatistics)
        user_director.count += value
        if user_director.count:
            user_director.save()
        else:
            user_director.delete()


def count_genre(movie, value, user):
    genres = movie.genre.all()
    for genre in genres:
        user_genre, created = UserGenre.objects.get_or_create(genre=genre,
                                                              user_statistics=user.userstatistics)
        user_genre.count += value
        if user_genre.count:
            user_genre.save()
        else:
            user_genre.delete()


def count_nation(movie, value, user):
    nations = movie.nation_code.all()
    for nation in nations:
        user_nation, created = UserNation.objects.get_or_create(nation=nation,
                                                                user_statistics=user.userstatistics)
        user_nation.count += value
        if user_nation.count:
            user_nation.save()
        else:
            user_nation.delete()


def count_movie(value, user):
    user_statistics, created = UserStatistics.objects.get_or_create(user=user)

    user_statistics.movie_count += value
    user_statistics.save()


def count_score(user_score, value, user):
    user_statistics_score, created = UserScores.objects.get_or_create(user_statistics=user.userstatistics)
    user_statistics_score.set_score(user_score, value)


@transaction.atomic
def count_all(movie, user_score, value, user):
    count_movie(value, user)
    count_score(user_score, value, user)

    weighted_value = user_score / 5 * value
    count_actor(movie, weighted_value, user)
    count_director(movie, weighted_value, user)
    count_genre(movie, weighted_value, user)
    count_nation(movie, weighted_value, user)


