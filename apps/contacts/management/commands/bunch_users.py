from django.core.management.base import BaseCommand

from apps.users import models as user_models
from apps.contacts import models as contact_models


class Command(BaseCommand):

    def handle(self, *args, **options):
        accounts = user_models.Account.objects.all()
        contacts = contact_models.Contact.objects.all()
        for account in accounts:
            self.search_account_in_contacts(account, contacts)

    def search_account_in_contacts(self, account, contacts):
        for contact in contacts:
            self.add_account_to_contact(account, contact)

    @staticmethod
    def add_account_to_contact(account, contact):
        if account.phone == contact.phone and account not in contact.accounts:
            contact.accounts.add(account)
