from django_filters import rest_framework as filters

from events import models


class EventFilter(filters.FilterSet):
    completed = filters.BooleanFilter(field_name='completed_at', lookup_expr='isnull')

    class Meta:
        model = models.Event
        fields = ('completed',)
