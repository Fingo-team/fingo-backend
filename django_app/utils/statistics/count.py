from django.db import transaction

from user_statistics.models import UserActor, UserDirector

__all__ = [
    'count_all',
]


def count_actor(movie, value, user):
    actors = movie.actor.all()
    for actor in actors:
        user_actor, created = UserActor.objects.get_or_create(actor=actor,
                                                              user_statistics=user.userstatistics)
        user_actor.set_count(value)


def count_director(movie, value, user):
    directors = movie.director.all()
    for director in directors:
        user_director, created = UserDirector.objects.get_or_create(director=director,
                                                                    user_statistics=user.userstatistics)
        user_director.count += value
        user_director.save()


@transaction.atomic
def count_all(movie, user_score, value, user):
    user.userstatistics.count(value)
    user.userstatistics.userscores.set_score(user_score, value)
    count_actor(movie, value, user)
    count_director(movie, value, user)


