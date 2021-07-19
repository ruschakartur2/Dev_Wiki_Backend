from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django_extensions.db.fields import RandomCharField
from simple_history.models import HistoricalRecords

from DevWikiBackend import settings
from core.managers import users
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return 'Tag[id:{id}, title: {title}]'.format(id=self.id, title=self.title)


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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120, blank=False)
    last_name = models.CharField(max_length=120, blank=False)
    phone = models.CharField(max_length=120, blank=False)

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.email)


class Article(models.Model):
    title = models.CharField(verbose_name=_("Article's title"), max_length=255)
    created_at = models.DateTimeField(verbose_name=_("Article's created time"), auto_now=True)
    author = models.ForeignKey(get_user_model(),
                               verbose_name=_("Article's author"),
                               on_delete=models.CASCADE)
    body = models.TextField(verbose_name=_('Body'))
    slug = RandomCharField(length=4,
                           include_alpha=False,
                           unique=True,
                           verbose_name=_("Article's slug field to url search"))
    tags = models.ManyToManyField(Tag, related_name='articles')
    previous_version = HistoricalRecords(verbose_name=_("Article's previous version"))
    visits = models.IntegerField(default=0)

    def __str__(self):
        """Function to naming model"""
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article,
                                verbose_name=_("Comment to article"),
                                related_name='comments',
                                on_delete=models.CASCADE)
    content = models.TextField(verbose_name=_("Comment's text"))
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_("Comment's author"),
    )
    parent = models.ForeignKey('self',
                               blank=True,
                               on_delete=models.CASCADE,
                               null=True,
                               related_name='children',
                               verbose_name=_("Reply to comment"))
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Comment {}'.format(self.content)

    @property
    def owner(self):
        return self.author