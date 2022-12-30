from rest_framework import viewsets, filters

from events import models
from events import serializers
from events import filters as custom_filters


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class EventViewSet(viewsets.ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_class = custom_filters.EventFilter
    search_fields = ['title', 'category__title']
    ordering_fields = ['created_at', 'completed_at']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
