from rest_framework import viewsets

from events import models
from events import serializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
