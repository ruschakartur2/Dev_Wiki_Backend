from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db import models

from pkg.users.managers.users import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(verbose_name=_("User's status (online/offline)"), default=True)
    is_staff = models.BooleanField(verbose_name=_("User's admin status"), default=False)
    is_superuser = models.BooleanField(verbose_name=_("User's superuser status"), default=False)
    is_moder = models.BooleanField(verbose_name=_("User's moder status"), default=False)
    is_banned = models.BooleanField(verbose_name=_("User banned"), default=False)
    is_muted = models.BooleanField(verbose_name=_("User muted"), default=False)
    email = models.EmailField(verbose_name=_("User's email address"),
                              max_length=255,
                              unique=True)
    nickname = models.CharField(verbose_name=_("User's nickname"),
                                max_length=255,
                                blank=True,
                                null=True)
    image = models.ImageField(upload_to='user_images', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def __str__(self):
        """Function to naming model"""
        return self.email

