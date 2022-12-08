from django.utils import timezone
from django.conf import settings
from celery import shared_task

from accounts import models


@shared_task(name='delete_old_tokens')
def delete_old_tokens():
    past_date = timezone.now() - timezone.timedelta(hours=settings.TOKEN_EXPIRATION)
    models.VerificationToken.objects.filter(created_at__lte=past_date).delete()
