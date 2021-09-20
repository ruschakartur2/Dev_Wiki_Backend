import django_filters

from pkg.core.models import Tag


class TagFilter(django_filters.FilterSet):
    no_articles = django_filters.BooleanFilter(field_name='articles', label='No articles', lookup_expr='isnull')

    class Meta:
        model = Tag
        fields = ['no_articles', ]
