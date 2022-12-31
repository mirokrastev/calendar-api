import coreapi
import coreschema
from django_filters import rest_framework as filters

from events import models


class EventFilterBackend(filters.DjangoFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='category',
                location='query',
                required=False,
                schema=coreschema.String(
                    description='Category ID'
                ),
                type='string',
            ),
        ]


class EventFilter(filters.FilterSet):
    category = filters.UUIDFilter(label='Category ID')

    class Meta:
        model = models.Event
        fields = ('category',)
