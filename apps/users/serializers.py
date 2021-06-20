from rest_framework import serializers

from apps.users import models as user_models


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.Account
        exclude = ['sms_code', 'first_name', 'last_name', 'email',
                   'password', 'groups', 'user_permissions']


class AuthUserSerializer(serializers.Serializer):
    phone = serializers.CharField(min_length=10, max_length=15, required=True)
    code = serializers.CharField(min_length=4, max_length=4, required=False)
