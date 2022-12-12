import factory

from events import models
from accounts.tests.factories import UserFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Category
