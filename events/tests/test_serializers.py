from django.test import TestCase

from events import serializers
from events.tests.factories import CategoryFactory


class CategorySerializerTestcase(TestCase):
    def setUp(self):
        self.category = CategoryFactory()

    def test_serializer_response_single_object(self):
        serializer = serializers.CategorySerializer(self.category).data
        keys = {'id', 'title'}

        # Test if all serializer keys match keys
        self.assertSetEqual(set(serializer.keys()), keys)
