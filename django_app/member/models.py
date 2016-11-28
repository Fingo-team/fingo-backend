from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class FingoUserManager(BaseUserManager):
    def create_user(self, email, nickname, user_img=None, password=None):
        user = FingoUser(email=email,
                         nickname=nickname)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, nickname, password):
        user = FingoUser(email=email,
                         nickname=nickname)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user


class FingoUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100,
                                unique=True)
    level = models.IntegerField(default=1)
    exp = models.IntegerField(default=0)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_img = models.ImageField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("nickname",)

    objects = FingoUserManager()

    def get_short_name(self):
        return self.nickname

    def get_full_name(self):
        return self.nickname
