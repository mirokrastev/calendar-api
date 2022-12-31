from rest_framework import serializers


class UserForeignKey(serializers.PrimaryKeyRelatedField):
    """
    Limits the queryset to current user
    """

    def get_queryset(self):
        return super().get_queryset().filter(user=self.context['request'].user)
