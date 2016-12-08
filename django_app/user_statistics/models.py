from django.db import models
from member.models import FingoUser


class UserStatistics(models.Model):
    user = models.ForeignKey(FingoUser)
    movie_count = models.IntegerField(default=0)

    def __str__(self):
        return '{}: {}개 평가'.format(self.user.nickname, self.movie_count)

    def count(self, user_activities):
        self.movie_count = len(user_activities)
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

    def reset(self):
        self.point_five = 0
        self.one = 0
        self.one_point_five = 0
        self.two = 0
        self.two_point_five = 0
        self.three = 0
        self.three_point_five = 0
        self.four = 0
        self.four_point_five = 0
        self.five = 0
        self.save()

    def set_score(self, user_activity):
        if user_activity.score == 0.5:
            self.point_five += 1
        elif user_activity.score == 1.0:
            self.one += 1
        elif user_activity.score == 1.5:
            self.one_point_five += 1
        elif user_activity.score == 2.0:
            self.two += 1
        elif user_activity.score == 2.5:
            self.two_point_five += 1
        elif user_activity.score == 3.0:
            self.three += 1
        elif user_activity.score == 3.5:
            self.three_point_five += 1
        elif user_activity.score == 4.0:
            self.four += 1
        elif user_activity.score == 4.5:
            self.four_point_five += 1
        elif user_activity.score == 5.0:
            self.five += 1
        else:
            return
        self.save()
