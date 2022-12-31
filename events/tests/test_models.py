from django.test import TestCase
from django.db import IntegrityError

from events.tests.factories import (
    UserFactory,
    CategoryFactory,
)


class CategoryTestCase(TestCase):
    def test_category_uniqueness_per_user(self):
        user = UserFactory()
        CategoryFactory(user=user, title='Supermarket')

        with self.assertRaises(IntegrityError):
            CategoryFactory(user=user, title='Supermarket')
