from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase, APIClient

from apps.users import models as user_models


class AccountTests(APITestCase):
    def setUp(self):
        self.url = reverse('restapi:user-auth')
        self.phone = '+998935103518'

    def test_create_and_auth_account(self):
        res = self.client.post(self.url, {'phone': self.phone})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.user = user_models.Account.objects.last()
        self.assertEqual(self.user.phone, self.phone)
        self.code = self.user.sms_code
        res = self.client.post(self.url, {'phone': self.phone, 'code': self.code})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        token = Token.objects.get(user=self.user).key
        self.assertIn('token', res.data)
        self.assertEqual(res.data['token'], token)
