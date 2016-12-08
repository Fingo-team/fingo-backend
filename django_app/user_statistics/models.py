from django.db import models
from member.models import FingoUser
from movie.models import Actor


class UserStatistics(models.Model):
    user = models.OneToOneField(
        FingoUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    movie_count = models.IntegerField(default=0)

    def __str__(self):
        return '{}: {}개 평가'.format(self.user.nickname, self.movie_count)

    def count(self, value):
        self.movie_count += value
        self.save()


class UserScores(models.Model):
    user_statistics = models.OneToOneField(
        UserStatistics,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    point_five = models.IntegerField(default=0)
    one = models.IntegerField(default=0)
    one_point_five = models.IntegerField(default=0)
    two = models.IntegerField(default=0)
    two_point_five = models.IntegerField(default=0)
    three = models.IntegerField(default=0)
    three_point_five = models.IntegerField(default=0)
    four = models.IntegerField(default=0)
    four_point_five = models.IntegerField(default=0)
    five = models.IntegerField(default=0)

    def __str__(self):
        return '{}의 score'.format(self.user_statistics.user.nickname)

    def set_score(self, user_score, value):
        print('value: {}'.format(value))
        if user_score == 0.5:
            self.point_five += value
        elif user_score == 1.0:
            self.one += value
        elif user_score == 1.5:
            self.one_point_five += value
        elif user_score == 2.0:
            self.two += value
        elif user_score == 2.5:
            self.two_point_five += value
        elif user_score == 3.0:
            self.three += value
        elif user_score == 3.5:
            self.three_point_five += value
        elif user_score == 4.0:
            self.four += value
        elif user_score == 4.5:
            self.four_point_five += value
        elif user_score == 5.0:
            self.five += value
        else:
            return
        self.save()


class UserActors(models.Model):
    user = models.ForeignKey(FingoUser)
    actor = models.ForeignKey(Actor)