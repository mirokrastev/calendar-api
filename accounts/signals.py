from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail

from accounts import models


@receiver(post_save, sender=models.User)
def create_user_verification_token(instance, created, **kwargs):
    if not created or instance.is_active:
        return

    models.VerificationToken.objects.create(user=instance, type=models.VerificationToken.Types.ACCOUNT, silent=False)


@receiver(post_save, sender=models.VerificationToken)
def send_user_verification_email(instance, created, **kwargs):
    if not created or instance.silent:
        return

    context = {
        'name': instance.user.first_name or instance.user.username,
        'token': instance.token
    }

    email_content = render_to_string('email/account_activation.html', context)
    send_mail(subject='Verification Token',
              message=email_content,
              html_message=email_content,
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[instance.user.email])
