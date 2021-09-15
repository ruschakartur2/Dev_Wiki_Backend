from django.db import models


class State(models.IntegerChoices):
    POSTED = 1
    DELETED = 2
    REDACTION = 3


class Role(models.IntegerChoices):
    MEMBER = 1
    MODER = 2
    ADMIN = 3
