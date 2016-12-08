from django.db import transaction
__all__ = [
    'count_all',
]


@transaction.atomic
def count_all(user_score, value, user):
    user.userstatistics.count(value)
    user.userstatistics.userscores.set_score(user_score, value)

