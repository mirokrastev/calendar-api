from django.db import models

from base.models import BaseModel
from accounts.models import User


class Category(BaseModel):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f'{self.user} -> {self.title}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(fields=['title', 'user'], name='unique_category')
        ]
