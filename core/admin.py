from django.contrib import admin
from core import models

admin.site.register(models.User)
admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.Profile)
