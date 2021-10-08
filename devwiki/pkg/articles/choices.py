from django.db import models


class Status(models.IntegerChoices):
    POSTED = 1
    DELETED = 2
