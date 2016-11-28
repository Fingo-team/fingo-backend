from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=100)
    img = models.URLField()
    daum_code = models.CharField(max_length=50,
                                 unique=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100)
    img = models.URLField()
    daum_code = models.CharField(max_length=50,
                                    unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    actor = models.ManyToManyField(Actor,
                                   through="MovieActorDetail")
    director = models.ManyToManyField(Director)
    genre = models.CharField(max_length=50)
    story = models.TextField()
    img = models.URLField()
    viewer_cnt = models.IntegerField()
    frst_run_date = models.DateField()
    nation_code = models.CharField(max_length=50)
    naver_code = models.CharField(max_length=50)
    daum_code = models.CharField(max_length=50,
                                 unique=True)

    def __str__(self):
        return self.title


class MovieActorDetail(models.Model):
    movie = models.ForeignKey(Movie)
    actor = models.ForeignKey(Actor)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.movie


class StillCut(models.Model):
    img = models.URLField()
    movie = models.ForeignKey(Movie)

    def __str__(self):
        return self.movie