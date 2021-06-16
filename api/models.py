from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from api.managers.users import UserManager
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def __str__(self):
        return self.email


class Article(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    created_at = models.DateTimeField(verbose_name=_('Created time'), auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField(verbose_name=_('Body'))

    def __str__(self):
        return self.title
