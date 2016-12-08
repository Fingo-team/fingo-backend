from django.db import transaction
__all__ = [
    'count_all',
]


def count_all(user_activity, value, user):
    with transaction.atomic():
        count_movie(user_activity, value, user)
        count_score(user_activity, user)


@transaction.atomic
def count_movie(user_activity, value, user):
    user.userstatistics.userscores.set_score(user_activity, value)


@transaction.atomic
def count_score(user_activity, user):
    user.userstatistics.count(user_activity)
