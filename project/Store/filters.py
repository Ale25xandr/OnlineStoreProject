import django_filters
import requests
from django_filters import FilterSet, DateTimeFilter
from .models import Response, Ads
from django.forms import DateTimeInput


class AdsFilter(FilterSet):
    ads__Heading = django_filters.CharFilter(lookup_expr='icontains', label='Название')

    class Meta:
        model = Response
        fields = ['ads__Heading']


class AdsListSearch(FilterSet):
    Author__username = django_filters.CharFilter(lookup_expr='icontains', label='Автор')
    Heading = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')
    Category = django_filters.ChoiceFilter(lookup_expr='icontains', label='Категория', choices=Ads.category_title,
                                           empty_label='  ')
    added_after = DateTimeFilter(
        field_name='Date',
        lookup_expr='gt',
        label='Дата добавления (не позднее)',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = Ads
        fields = ['Heading', 'Category', 'Author__username', 'added_after']


class MyAdsListSearch(FilterSet):
    Heading = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')
    Category = django_filters.ChoiceFilter(lookup_expr='icontains', label='Категория', choices=Ads.category_title,
                                           empty_label='  ')
    added_after = DateTimeFilter(
        field_name='Date',
        lookup_expr='gt',
        label='Дата добавления (не позднее)',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = Ads
        fields = ['Heading', 'Category', 'added_after']

