from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Article(models.Model):
    title = models.CharField(verbose_name='Title', max_length=255)
    created_at = models.DateTimeField(verbose_name='Created time', auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField(verbose_name='Body')
