from django.contrib import admin
from django.contrib.auth.models import Group

from core import models


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at', 'tags']


admin.site.site_header = 'Admin panel'
admin.site.register(models.User)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
admin.site.register(models.Membership)
admin.site.unregister(Group)
