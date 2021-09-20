from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Article, Comment, Tag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at', 'tags']


admin.site.site_header = 'Admin panel'
admin.site.register(User)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.unregister(Group)
