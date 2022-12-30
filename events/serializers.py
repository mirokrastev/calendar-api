from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework import validators

from events import models


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Category
        fields = ('id', 'title', 'user')

        validators = [
            validators.UniqueTogetherValidator(
                models.Category.objects.all(),
                fields=('title', 'user'),
                message=_('Category duplication'),
            ),
        ]


class EventSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, source='category',
                                                     required=False,
                                                     queryset=models.Category.objects.all())
    category = CategorySerializer(read_only=True)

    class Meta:
        model = models.Event
        fields = ('id', 'category', 'category_id', 'title', 'user')
