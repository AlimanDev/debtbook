from django.db import models
from django.shortcuts import get_object_or_404

from apps.users import models as account_models


class Contact(models.Model):
    """ Юзер, на чьё имя будет вестись учёт долга. """
    class Meta:
        db_table = 'contacts'

    accounts = models.ManyToManyField(  # По умолчанию 1 аккаунт - тот кто его создал. Второй аккаунт взятый из phone
        account_models.Account, verbose_name='Аккаунты', related_name='contacts', blank=True)
    phone = models.CharField(
        'Номер телефона', max_length=250, blank=True)
    name = models.CharField(
        'Имя контакта', max_length=250)
    hide_for = models.ManyToManyField(
        account_models.Account, verbose_name='Скрыть для', blank=True)

    created_at = models.DateTimeField(
        'Дата создания', auto_now=True)
    updated_at = models.DateTimeField(
        'Дата изменения', auto_now_add=True)

    def get_account_from_contact(self):
        if not self.phone:
            return None
        try:
            account = account_models.Account.objects.get(phone=self.phone)
            return account
        except account_models.Account.DoesNotExist:
            return None

    def get_owner(self):
        return self.accounts.first()

    def add_contact_to_accounts(self):
        # Если имеется контакт в базе, сохраняем его в accounts
        if self.accounts.count() < 2 and self.get_account_from_contact():
            self.accounts.add(self.get_account_from_contact())
            # self.save(update_fields=['accounts'])  # TODO: на случай, если не сохраняется accounts

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.add_contact_to_accounts()


class Currency(models.Model):
    """ Денежная валюта """
    class Meta:
        db_table = 'currencies'

    name = models.CharField(
        'Имя валюты', max_length=3)


class Payment(models.Model):
    """ Таблица хранения долгов и возврата """
    class Meta:
        db_table = 'payments'

    DEBT = 0
    PAID = 1
    TYPE_PAYMENT = (
        (0, 'Debt'),
        (1, 'Paid'),
    )

    contact = models.ForeignKey(
        Contact, verbose_name='Контакт', related_name='payments', on_delete=models.CASCADE, null=True)
    type_payment = models.IntegerField(
        'Тип оплаты', choices=TYPE_PAYMENT, null=True)
    amount = models.DecimalField(
        'Сумма', max_digits=20, decimal_places=2)
    currency = models.ForeignKey(
        Currency, verbose_name='Валюта', on_delete=models.PROTECT, null=True)
    comment = models.TextField(
        'Комментарий', blank=True)
    created_at = models.DateTimeField(
        'Дата создания', auto_now=True)
    updated_at = models.DateTimeField(
        'Дата изменения', auto_now_add=True)
