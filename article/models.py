from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
from simple_history.models import HistoricalRecords
from django.utils.translation import ugettext_lazy as _


class Article(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    created_at = models.DateTimeField(verbose_name=_('Created time'), auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField(verbose_name=_('Body'))
    history = HistoricalRecords()

    def __str__(self):
        return self.title
