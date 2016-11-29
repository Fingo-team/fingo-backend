from django.db import models
from member.models import FingoUser
from movie.models import Movie


class UserActivity(models.Model):
    user = models.ForeignKey(FingoUser)
    movie = models.ForeignKey(Movie)
    comment = models.CharField(max_length=200, blank=True)
    score = models.FloatField(null=True)
    watched_movie = models.BooleanField(default=False)
    wish_movie = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "movie",)

    def __str__(self):
        return "{} : {}".format(self.user.nickname, self.movie.title)
