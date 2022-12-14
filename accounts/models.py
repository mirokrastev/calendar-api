from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class User(BaseModel, AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return self.username


class VerificationToken(BaseModel):
    class Types(models.TextChoices):
        ACCOUNT = ('account', 'Account Verification')
        PASSWORD = ('password', 'Password Reset')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_tokens')
    token = models.CharField(max_length=128)
    type = models.CharField(max_length=32, choices=Types.choices)
    silent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        from accounts.services import token_service

        if not self.token:
            self.token = token_service[self.type].generate(self.user)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user} -> {self.type}'
