from django.contrib import admin

from .models import Article, ArticleRating, ArticleVisits, Comment, Tag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at', 'tags', 'rating']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleRating)
admin.site.register(ArticleVisits)
admin.site.register(Comment)
admin.site.register(Tag)
