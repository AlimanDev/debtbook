from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Account(AbstractUser):
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        db_table = 'accounts'

    avatar = models.ImageField(
        'Аватарка', upload_to='users/avatars/', blank=True)
    username = models.CharField(
        'Имя пользователя', max_length=250, unique=False, blank=True)
    phone = models.CharField(
        'Номер телефора', max_length=250, unique=True)
    sms_code = models.CharField(
        'СМС код', max_length=4, blank=True, null=True)

    USERNAME_FIELD = 'phone'
    objects = UserManager()
    REQUIRED_FIELDS = ['username']
