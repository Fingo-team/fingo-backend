from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
from movie.models import Movie
from passlib.hash import pbkdf2_sha512
from apis.mail import send_auth_mail


class FingoUserManager(BaseUserManager):
    def create_userhash(self, user):
        hashed_email = pbkdf2_sha512.using(rounds=8000, salt_size=20).hash(user.email)[:40]
        UserHash.objects.create(user=user,
                                hashed_email=hashed_email+settings.SECRET_KEY)

        send_auth_mail.send_activation_mail(user_email=user.email,
                                            hashed_email=hashed_email)

    def create_user(self, email, nickname, user_img=None, password=None):
        user = FingoUser(email=email,
                         nickname=nickname)
        user.set_password(password)
        user.save()

        self.create_userhash(user)

        return user

    def create_superuser(self, email, nickname, password):
        user = FingoUser(email=email,
                         nickname=nickname)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save()

        return user

    def create_facebook_user(self, facebook_id, nickname, password=None):
        user = FingoUser(email='{}@fingo.com'.format(facebook_id),
                         nickname=nickname,
                         facebook_id=facebook_id)
        user.is_facebook = True
        user.is_active = True
        user.set_password(password)
        user.save()
        return user


class FingoUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    user_img = models.ImageField(blank=True,
                                 upload_to="user_img")
    cover_img = models.ImageField(blank=True,
                                  upload_to="user_cover_img")
    activities = models.ManyToManyField(Movie,
                                        through="fingo_statistics.UserActivity")

    cover_img = models.ImageField(blank=True)
    # facebook_login
    facebook_id = models.CharField(max_length=50, blank=True)
    is_facebook = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("nickname",)

    objects = FingoUserManager()

    def get_short_name(self):
        return self.nickname

    def get_full_name(self):
        return self.nickname


class UserHash(models.Model):
    user = models.ForeignKey(FingoUser)
    hashed_email = models.CharField(max_length=200)
