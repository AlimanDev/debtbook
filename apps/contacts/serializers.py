from rest_framework import serializers

from apps.contacts import models as contact_models


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact_models.Contact
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = contact_models.Payment
        fields = '__all__'
