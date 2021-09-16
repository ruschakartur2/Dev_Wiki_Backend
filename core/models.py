from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from django_extensions.db.fields import RandomCharField
from simple_history.models import HistoricalRecords
from django.core.validators import RegexValidator

from core.managers import users
from .utils.choices import State
from django.utils.translation import ugettext_lazy as _


alphaValidator = RegexValidator(r'[A-Za-zwА-Яа-яІіЄєЇї]+$', 'That field can contain only letters')


class User(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(verbose_name=_("User's status (online/offline)"), default=True)
    is_staff = models.BooleanField(verbose_name=_("User's admin status"), default=False)
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

    objects = users.UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def __str__(self):
        """Function to naming model"""
        return self.email


class Tag(models.Model):
    title = models.CharField(max_length=64, verbose_name=_("Tag's title"), unique=True, validators=[alphaValidator])
    description = models.CharField(max_length=255, verbose_name=_("Tag's description"))

    def __str__(self):
        return 'Tag[id:{id}, title: {title}]'.format(id=self.id, title=self.title)


class Article(models.Model):
    title = models.CharField(verbose_name=_("Article's title"),
                             max_length=255,
                             validators=[MinLengthValidator(1), alphaValidator])
    created_at = models.DateTimeField(verbose_name=_("Article's created time"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Article's updated time"), auto_now=True)
    author = models.ForeignKey(get_user_model(),
                               verbose_name=_("Article's author"),
                               on_delete=models.CASCADE)
    body = models.TextField(verbose_name=_("Article's body"), validators=[MinLengthValidator(10)])
    slug = RandomCharField(length=4,
                           include_alpha=False,
                           unique=True,
                           verbose_name=_("Article's slug field to url search"))
    tags = models.ManyToManyField(Tag,
                                  related_name='articles', )
    visits = models.IntegerField(default=0)
    status = models.PositiveSmallIntegerField(
        choices=State.choices,
        default=State.POSTED,
        verbose_name=_("Article's status (Deleted/Posted)")
    )
    previous_version = HistoricalRecords(verbose_name=_("Article's previous version"))

    def __str__(self):
        """Function to naming model"""
        return self.title



class Comment(models.Model):
    article = models.ForeignKey(Article,
                                verbose_name=_("Comment to article"),
                                related_name='comments',
                                on_delete=models.CASCADE)
    content = models.TextField(verbose_name=_("Comment's text"), blank=False, null=False)
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment {}'.format(self.content)

    @property
    def owner(self):
        return self.author
