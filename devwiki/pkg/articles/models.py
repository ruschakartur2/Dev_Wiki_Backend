from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator

from django.utils.translation import ugettext_lazy as _
from pkg.articles.choices import Status
from django_extensions.db.fields import AutoSlugField

alphaValidator = RegexValidator(r'[A-Za-zwА-Яа-яІіЄєЇї]+$', 'That field can contain only letters')


class Article(models.Model):
    title = models.CharField(verbose_name=_("Article's title"),
                             max_length=255,
                             unique=True,
                             validators=[MinLengthValidator(1), alphaValidator])
    created_at = models.DateTimeField(verbose_name=_("Article's created time"),
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Article's updated time"),
                                      auto_now=True)
    author = models.ForeignKey(get_user_model(),
                               verbose_name=_("Article's author"),
                               on_delete=models.DO_NOTHING)
    body = models.TextField(verbose_name=_("Article's body"), validators=[MinLengthValidator(10)])
    slug = AutoSlugField(populate_from='title',
                         blank=True,
                         null=True,
                         verbose_name=_("Article's slug"))
    tags = models.ManyToManyField('Tag',
                                  blank=True,
                                  null=True,
                                  verbose_name=_("Article's tags"))
    visits = models.OneToOneField('ArticleVisits',
                                  on_delete=models.CASCADE,
                                  verbose_name=_("Article's visits number"),
                                  null=True,
                                  blank=True)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.POSTED,
        verbose_name=_("Article's status (Deleted/Posted)")
    )

    def __str__(self):
        """Function to naming model"""
        return self.title


class ArticleVisits(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return f"{self.article.title} - {self.number}"


class ArticleRating(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Rating user"),
        on_delete=models.DO_NOTHING,
    )
    article = models.ForeignKey('Article',
                                verbose_name=_("Rating article"),
                                on_delete=models.CASCADE,
                                related_name="rating")
    star = models.PositiveSmallIntegerField(verbose_name=_("Rating star"),
                                            validators=[MaxValueValidator(5)],
                                            default=0)

    def __str__(self):
        return f"{self.star} - {self.article.title}"


class Comment(models.Model):
    article = models.ForeignKey(Article,
                                verbose_name=_("Comment to article"),
                                related_name='comments',
                                on_delete=models.CASCADE)
    content = models.TextField(verbose_name=_("Comment's text"),
                               blank=False,
                               null=False)
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
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.POSTED,
        verbose_name=_("Comment's status (Deleted/Posted)")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment {self.content}'

    @property
    def owner(self):
        return self.author


class Tag(models.Model):
    name = models.CharField(max_length=64,
                            verbose_name=_("Tag's title"),
                            unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name
