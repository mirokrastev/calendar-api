from django.db import models
from django.db.models import Q, F

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
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['title', 'user'], name='unique_category')
        ]


class Event(BaseModel):
    title = models.CharField(max_length=256)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='events')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f'{self.user} -> {self.title}'

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(check=Q(start_date__lt=F('end_date')),
                                   name='start_date_before_end_date')
        ]
