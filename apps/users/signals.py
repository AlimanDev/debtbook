from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from apps.users import models as user_models


@receiver(signal=post_save, sender=user_models.Account)
def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
