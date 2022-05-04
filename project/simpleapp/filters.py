from django_filters import FilterSet, DateFilter, CharFilter
import django.forms


class NewsArticleFilter(FilterSet):
    date = DateFilter(
        field_name='news_data',
        lookup_expr='exact',
        label="Дата",
        widget=django.forms.DateInput(attrs={'type': 'date'})
    )
    author = CharFilter(
        field_name='author',
        lookup_expr='icontains',
        label="Автор",
    )


