from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django_extensions.db.fields import RandomCharField
from simple_history.models import HistoricalRecords

from api.managers import users
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_("User's email address"), max_length=255, unique=True)
    is_active = models.BooleanField(verbose_name=_("User's status (online/offline)"), default=True)
    is_staff = models.BooleanField(verbose_name=_("User's admin status"), default=False)

    objects = users.UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def __str__(self):
        """Function to naming model"""
        return self.email


class Article(models.Model):
    title = models.CharField(verbose_name=_("Article's title"), max_length=255)
    created_at = models.DateTimeField(verbose_name=_("Article's created time"), auto_now=True)
    author = models.ForeignKey(get_user_model(),
                               verbose_name=_("Article's author"),
                               on_delete=models.CASCADE)
    body = models.TextField(verbose_name=_('Body'))
    previous_version = HistoricalRecords(verbose_name=_("Article's previous version"))
    slug = RandomCharField(length=4,
                           include_alpha=False,
                           unique=True,
                           verbose_name=_("Article's slug field to url search"))

    def __str__(self):
        """Function to naming model"""
        return self.title

